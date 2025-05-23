from sqlalchemy import Column, ForeignKey, String, DateTime, Numeric
from sqlalchemy.dialects.mysql import INTEGER
from app.config.database import Base

class Flight(Base):
    __tablename__ = "flights"

    id = Column(INTEGER(unsigned=True), primary_key=True, index=True,autoincrement=True,nullable=False)
    flight_number = Column(String(50), nullable=False)
    airline_name = Column(String(50), nullable=False)
    departure_airport_id = Column(INTEGER(unsigned=True), ForeignKey("airports.id"), nullable=False)
    arrival_airport_id = Column(INTEGER(unsigned=True), ForeignKey("airports.id"), nullable=False)
    departure_time = Column(DateTime, nullable=False)
    arrival_time = Column(DateTime, nullable=False)
    available_seats = Column(INTEGER(unsigned=True), nullable=False)