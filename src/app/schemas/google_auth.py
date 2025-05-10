from pydantic import BaseModel
from typing import Optional

class UserResponse(BaseModel):
    id: int
    full_name: str
    email: str

class AuthResponse(BaseModel):
    message: str
    access_token: str
    token_type: str
    user: UserResponse