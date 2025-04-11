from sqlalchemy import Column, Integer, String
from app.config.database import Base

class Airport(Base):
    __tablename__ = "airports"

    id = Column(Integer(unsigned=True), primary_key=True, index=True, autoincrement=True)
    code = Column(String(10), nullable=False, unique=True)
    name = Column(String(100), nullable=False)
    city = Column(String(50), nullable=True)
    country = Column(String(50), nullable=True)