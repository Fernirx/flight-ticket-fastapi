import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.config.database import Base
class VerificationCode(Base):
    __tablename__ = "verification_codes"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), ForeignKey("users.email", ondelete="CASCADE"), nullable=False)
    code = Column(String(20), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow) 
    user = relationship("User", back_populates="verification_codes")

