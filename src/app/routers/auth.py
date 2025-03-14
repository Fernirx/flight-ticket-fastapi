from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.schemas import VerifyOTPRequest, UserLoginRequest, ResetPasswordRequest
from app.config.database import get_db
from app.service.auth import verify_otp_service, login_user, reset_password_service

router = APIRouter(prefix="/auth", tags=["Authentication"])
@router.post("/login/")
def login(request: UserLoginRequest, db: Session = Depends(get_db)):
    return login_user(request, db)

@router.post("/reset-password/")
def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    return reset_password_service(request, db)
@router.post("/verify-otp/")
def verify_otp(request: VerifyOTPRequest, db: Session = Depends(get_db)):
    return verify_otp_service(request, db)