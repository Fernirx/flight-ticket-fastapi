from pydantic import BaseModel, EmailStr

class VerifyOTPRequest(BaseModel):
    email: EmailStr 
    otp: str 
    
class ResendOTPRequest(BaseModel):
    email: EmailStr