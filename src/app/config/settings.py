from pydantic_settings import BaseSettings
from pydantic import EmailStr

class Settings(BaseSettings):
    """Settings for the application."""

    # Database settings
    DATABASE_URL: str
    DATABASE_NAME: str
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_HOST: str
    DATABASE_PORT: int
    
    #JWT settings
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    
    # Email settings
    SMTP_SERVER: str
    SMTP_PORT: int
    EMAIL_SENDER: EmailStr
    EMAIL_PASSWORD: str

    class Config:
        """Configuration for the settings."""
        env_file = "app/.env"
        env_file_encoding = "utf-8"
        
settings = Settings()
        
    
