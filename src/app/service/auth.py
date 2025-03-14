from datetime import timedelta, datetime
import secrets
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.models import User, VerificationCode
from app.service.security import hash_password, verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

def login_user(request, db: Session):
    user = db.query(User).filter(User.username == request.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="Tài khoản không tồn tại")
    if not verify_password(request.password, user.password_hash, user.salt):
        raise HTTPException(status_code=401, detail="Mật khẩu không đúng")
    if not user.is_email_verified:
        raise HTTPException(status_code=403, detail="Email chưa được xác thực")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"message": "Đăng nhập thành công", "access_token": access_token, "token_type": "bearer"}

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
        raise HTTPException(status_code=400, detail="Không tìm thấy tài khoản. Vui lòng đăng ký lại.")
    
    user.is_email_verified = True
    db.delete(verification_entry)
    db.commit()
    
    return {"message": "Xác thực OTP thành công! Tài khoản đã được kích hoạt."}