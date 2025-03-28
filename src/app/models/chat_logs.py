from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, Text
from app.config.database import Base

class ChatLog(Base):
    __tablename__ = "chat_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    session_id = Column(String(255), nullable=True)
    message = Column(Text, nullable=True)
    bot_response = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False)