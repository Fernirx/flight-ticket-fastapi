from datetime import timedelta, datetime
import secrets
from app.schemas.google_auth import AuthResponse
import httpx
from app.config.settings import settings
from app.schemas.user import UserResponse
from fastapi import HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.verification_code import VerificationCode
from app.service.email_otp import generate_otp, send_otp_email
from app.service.security import hash_password, verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, is_valid_email

GOOGLE_CLIENT_ID = settings.GOOGLE_CLIENT_ID
GOOGLE_CLIENT_SECRET = settings.GOOGLE_CLIENT_SECRET
GOOGLE_REDIRECT_URI = settings.GOOGLE_REDIRECT_URI

def login_user(request, db: Session):
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Tài khoản không tồn tại")
    if not verify_password(request.password, user.password_hash, user.salt):
        raise HTTPException(status_code=401, detail="Mật khẩu không đúng")
    if not user.is_email_verified:
        raise HTTPException(status_code=403, detail="Email chưa được xác thực")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    user_response = UserResponse(id=user.id, full_name=user.full_name, email=user.email)
    return {
        "message": "Đăng nhập thành công", 
        "access_token": access_token, 
        "token_type": "bearer",
        "user": user_response
    }

def create_google_login_url(request: Request):
    client_id = GOOGLE_CLIENT_ID
    redirect_uri = GOOGLE_REDIRECT_URI
    authorization_url = "https://accounts.google.com/o/oauth2/v2/auth"
    scope = ["openid", "email", "profile"]
    auth_url = httpx.URL(authorization_url, params={
        "client_id": client_id,
        "redirect_uri": str(redirect_uri),  # Chuyển URL thành string
        "scope": " ".join(scope),
        "response_type": "code",
        "access_type": "offline",
    })
    return RedirectResponse(auth_url)
    
async def handle_google_callback(code, db: Session):
    token_data = {
        'code': code,
        'client_id': GOOGLE_CLIENT_ID,
        'client_secret': GOOGLE_CLIENT_SECRET,
        'redirect_uri': GOOGLE_REDIRECT_URI,
        'grant_type': 'authorization_code',
    }

    try:
        async with httpx.AsyncClient() as client:
            # Trao đổi code để lấy token
            token_resp = await client.post(
                "https://accounts.google.com/o/oauth2/token",
                data=token_data,
                headers={'Content-Type': 'application/x-www-form-urlencoded'}
            )
            token_resp.raise_for_status()
            token = token_resp.json()
            access_token = token.get('access_token')
            if not access_token:
                raise HTTPException(status_code=400, detail="Không lấy được access token từ Google")

            # Lấy thông tin người dùng
            user_info_resp = await client.get(
                "https://www.googleapis.com/oauth2/v1/userinfo",
                headers={'Authorization': f"Bearer {access_token}"}
            )
            user_info_resp.raise_for_status()
            user_info = user_info_resp.json()

        # Kiểm tra xem người dùng đã tồn tại trong cơ sở dữ liệu chưa
        user = db.query(User).filter_by(email=user_info.get('email')).first()
        if not user:
            new_user = User(
                full_name=user_info.get('name'),
                email=user_info.get('email'),
                password_hash=None,
                salt=None,
                is_email_verified=True
            )
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            user = new_user

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)

        # Lưu session
        return AuthResponse(
            message="Đăng nhập bằng Google thành công",
            access_token=access_token,
            token_type="bearer",
            user=UserResponse(
                id=user.id, 
                full_name=user.full_name, 
                email=user.email
            ).dict()
        )

    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail=f"Lỗi khi lấy token hoặc thông tin người dùng: {e}")

def register_user_service(request, db: Session):
    if len(request.password) < 8:
        raise HTTPException(status_code=400, detail="Mật khẩu phải có ít nhất 8 ký tự")
    if not is_valid_email(request.email):
        raise HTTPException(status_code=400, detail="Email không hợp lệ")
    if db.query(User).filter_by(email=request.email).first():
        raise HTTPException(status_code=400, detail="Email đã được sử dụng")
    
    salt = secrets.token_hex(16)
    hashed_password = hash_password(request.password, salt)
    new_user = User(
        full_name=request.full_name,
        email=request.email,
        password_hash=hashed_password,
        salt=salt,
        is_email_verified=False
    )
    db.add(new_user)
    
    otp_code = generate_otp()  # Hàm tạo OTP được định nghĩa trong service_email
    send_otp_email(request.email, otp_code)  # Gửi OTP qua email
    
    # Xóa OTP cũ nếu có
    otp_entry = db.query(VerificationCode).filter_by(email=request.email).first()
    if otp_entry:
        db.delete(otp_entry)
    new_otp = VerificationCode(email=request.email, code=otp_code, created_at=datetime.utcnow())
    db.add(new_otp)
    db.commit()
    
    return {"message": "Mã OTP đã được gửi"}

def reset_password_service(request, db: Session):
    if request.new_password != request.confirm_password:
        raise HTTPException(status_code=400, detail="Xác nhận mật khẩu không khớp")
    if len(request.new_password) < 8:
        raise HTTPException(status_code=400, detail="Mật khẩu phải có ít nhất 8 ký tự")
    
    user = db.query(User).filter_by(email=request.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Email không tồn tại")
    
    salt = secrets.token_hex(16)
    user.salt = salt
    user.password_hash = hash_password(request.new_password, salt)
    db.commit()
    return {"message": "Mật khẩu đã được đặt lại thành công"}

def verify_otp_service(request, db: Session):
    verification_entry = db.query(VerificationCode).filter_by(email=request.email).first()
    if not verification_entry or verification_entry.code != request.otp:
        raise HTTPException(status_code=400, detail="Mã OTP không chính xác hoặc không tồn tại")
    
    otp_expiry_time = verification_entry.created_at + timedelta(minutes=5)
    if datetime.utcnow() > otp_expiry_time:
        db.delete(verification_entry)
        db.commit()
        raise HTTPException(status_code=400, detail="Mã OTP đã hết hạn. Vui lòng yêu cầu lại mã mới.")
    
    user = db.query(User).filter_by(email=request.email).first()
    if not user:
        raise HTTPException(status_code=400, detail="Không tìm thấy tài khoản")
    
    user.is_email_verified = True
    db.delete(verification_entry)
    db.commit()  
    return {"message": "Xác thực OTP thành công!"}

def resent_otp_service(request, db: Session):
    user = db.query(User).filter_by(email=request.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Không tìm thấy tài khoản")
    
    otp_code = generate_otp()
    send_otp_email(request.email, otp_code)
    
    # Xóa OTP cũ nếu có
    otp_entry = db.query(VerificationCode).filter_by(email=request.email).first()
    if otp_entry:
        db.delete(otp_entry)
        db.flush()
    new_otp = VerificationCode(email=request.email, code=otp_code, created_at=datetime.utcnow())
    db.add(new_otp)
    db.commit()
    return {"message": "Mã OTP mới đã được gửi qua email. Vui lòng kiểm tra hộp thư!"}