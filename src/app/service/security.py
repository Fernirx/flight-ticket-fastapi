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
def create_access_token(data: dict, expires_delta: timedelta = None):
    if expires_delta is None:
        expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = data.copy()
    to_encode.update({"exp": datetime.now(datetime.timezone.utc) + expires_delta})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

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
