from pydantic import BaseModel, EmailStr

class UserLoginRequest(BaseModel):
    email: str
    password: str

class ResetPasswordRequest(BaseModel):
    email: EmailStr
    new_password: str
    confirm_password: str
    
class UserRegisterRequest(BaseModel):
    full_name:str
    email: EmailStr
    password: str