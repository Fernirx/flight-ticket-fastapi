from http.client import HTTPException
from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.schemas.otp import VerifyOTPRequest, ResendOTPRequest
from app.schemas.user import UserLoginRequest, ResetPasswordRequest, UserRegisterRequest
from app.config.database import get_db
from app.service.auth import verify_otp_service, login_user, reset_password_service, register_user_service, resent_otp_service, create_google_login_url, handle_google_callback

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login/")
def login(request: UserLoginRequest, db: Session = Depends(get_db)):
    return login_user(request, db)

@router.get("/google/login/")
async def google_login(request: Request):
    return create_google_login_url(request)

@router.get("/google/callback/")
async def google_callback(request: Request, code: str, db: Session = Depends(get_db)):
    response = await handle_google_callback(code, db)
    if response is not None:
        # Truy cập trực tiếp các thuộc tính của `response.user`
        redirect_url = f"https://dcwizard.io.vn?access_token={response.access_token}&full_name={response.user.full_name}&email={response.user.email}"
        return RedirectResponse(url=redirect_url)
    else:
        raise HTTPException(status_code=400, detail="Failed to authenticate with Google.")

@router.post("/reset-password/")
def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    return reset_password_service(request, db)

@router.post("/verify-otp/")
def verify_otp(request: VerifyOTPRequest, db: Session = Depends(get_db)):
    return verify_otp_service(request, db)

@router.post("/register_user/")
def register(request: UserRegisterRequest, db: Session = Depends(get_db)):
    return register_user_service(request, db)

@router.post("/resent-otp/")
def resent_otp(request: ResendOTPRequest, db: Session = Depends(get_db)):
    return resent_otp_service(request, db)
