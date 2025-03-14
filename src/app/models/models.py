import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.config.database import Base,engine

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    salt = Column(String(32), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    is_email_verified = Column(Boolean, default=False)

    verification_codes = relationship("VerificationCode", back_populates="user")

class VerificationCode(Base):
    __tablename__ = "verification_codes"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), ForeignKey("users.email", ondelete="CASCADE"), nullable=False)
    code = Column(String(20), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow) 

    user = relationship("User", back_populates="verification_codes")
