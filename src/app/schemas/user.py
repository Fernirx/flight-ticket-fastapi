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

class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    
class LoginResponse(BaseModel):
    message: str
    access_token: str
    token_type: str
    user: UserResponse