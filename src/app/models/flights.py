from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, Numeric
from app.config.database import Base

class Flight(Base):
    __tablename__ = "flights"

    id = Column(Integer(unsigned=True), primary_key=True, index=True,autoincrement=True,nullable=False)
    flight_number = Column(String(50), nullable=False)
    departure_airport_id = Column(Integer(unsigned=True), ForeignKey("airports.id"), nullable=False)
    arrival_airport_id = Column(Integer(unsigned=True), ForeignKey("airports.id"), nullable=False)
    departure_time = Column(DateTime, nullable=False)
    base_price = Column(Numeric(10,2), nullable=False)