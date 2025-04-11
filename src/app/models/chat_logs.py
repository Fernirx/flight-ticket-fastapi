from sqlalchemy import Column, ForeignKey, String, DateTime, Text,func
from sqlalchemy.dialects.mysql import INTEGER
from app.config.database import Base

class ChatLog(Base):
    __tablename__ = "chat_logs"

    id = Column(INTEGER(unsigned=True), primary_key=True, index=True,autoincrement=True)
    user_id = Column(INTEGER(unsigned=True), ForeignKey("users.id"), nullable=True)
    session_id = Column(String(100), nullable=False)
    message = Column(Text, nullable=False)
    bot_response = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=True,server_default=func.now())