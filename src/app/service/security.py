from datetime import datetime, timedelta
from passlib.context import CryptContext
import jwt
import re

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
# Hàm tạo JWT token
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    to_encode.update({"exp": datetime.utcnow() + expires_delta})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Hàm hash mật khẩu
def hash_password(password: str, salt: str) -> str:
    return pwd_context.hash(password + salt)

# Hàm kiểm tra mật khẩu
def verify_password(plain_password, hashed_password, salt):
    return pwd_context.verify(plain_password + salt, hashed_password)

# Kiểm tra email hợp lệ
def is_valid_email(email: str) -> bool:
    return re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email) is not None
