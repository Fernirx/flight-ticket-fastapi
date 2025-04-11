from sqlalchemy import Column, ForeignKey, DateTime,func
from sqlalchemy.dialects.mysql import INTEGER
from app.config.database import Base

class ShoppingCart(Base):
    __tablename__ = "shopping_carts"

    id = Column(INTEGER(unsigned=True), primary_key=True, index=True,autoincrement=True,nullable=False)
    user_id = Column(INTEGER(unsigned=True), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, nullable=True,server_default=func.now())
    updated_at = Column(DateTime, nullable=True,server_default=func.now())