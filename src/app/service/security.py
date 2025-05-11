from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime, timedelta
from passlib.context import CryptContext
import jwt
from email_validator import validate_email, EmailNotValidError
from app.config.settings import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# SECRET_KEY is used as the cryptographic key for signing JWT tokens.
# It is critical to keep this key confidential to ensure the security of the tokens.
SECRET_KEY = settings.SECRET_KEY
# ALGORITHM is the algorithm used for signing the JWT tokens.
ALGORITHM = settings.ALGORITHM
# Function to create JWT token
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
# Hàm tạo JWT token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login/")

def create_access_token(data: dict, expires_delta: timedelta = None):
    if expires_delta is None:
        expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = data.copy()
    to_encode.update({"exp": datetime.utcnow() + expires_delta})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_admin(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Không thể xác thực")
        return email
    except JWTError:
        raise HTTPException(status_code=401, detail="Token không hợp lệ")

# Hàm hash mật khẩu
def hash_password(password: str, salt: str) -> str:
    return pwd_context.hash(password + salt)

# Hàm kiểm tra mật khẩu
def verify_password(plain_password, hashed_password, salt):
    return pwd_context.verify(plain_password + salt, hashed_password)

# Kiểm tra email hợp lệ
def is_valid_email(email: str) -> bool:
    try:
        validate_email(email)
        return True
    except EmailNotValidError:
        return False
