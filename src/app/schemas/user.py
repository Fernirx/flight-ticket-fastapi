from pydantic import BaseModel, EmailStr

class UserLoginRequest(BaseModel):
    username: str
    password: str

class ResetPasswordRequest(BaseModel):
    email: EmailStr
    new_password: str
    confirm_password: str
    
class UserLoginRequest(BaseModel):
    username: str
    password: str
    
class VerifyOTPRequest(BaseModel):
    email: EmailStr
    otp: str