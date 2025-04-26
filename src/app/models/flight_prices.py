from sqlalchemy import Column,Enum,Numeric, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER
from app.config.database import Base

class FlightPrice(Base):
    __tablename__ = "flight_prices"

    id = Column(INTEGER(unsigned=True), primary_key=True, index=True, autoincrement=True, nullable=False)
    flight_id = Column(INTEGER(unsigned=True), ForeignKey("flights.id"), nullable=False)
    ticket_class_id = Column(INTEGER(unsigned=True), ForeignKey("ticket_classes.id"), nullable=False)
    adult_price = Column(Numeric(10, 2), nullable=False)
    child_price = Column(Numeric(10, 2), nullable=False)
    infant_price = Column(Numeric(10, 2), nullable=False)