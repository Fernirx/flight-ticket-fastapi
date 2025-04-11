from sqlalchemy import Column, Integer, ForeignKey,Enum,Numeric
from sqlalchemy.orm import relationship
from app.config.database import Base


class BookingItem(Base):
    __tablename__ = "booking_items"

    id = Column(Integer(unsigned=True), primary_key=True, index=True)
    booking_id = Column(Integer(unsigned=True), ForeignKey("bookings.id"), nullable=False)
    trip_type = Column(Enum("one way", "round trip"), nullable=False)
    departure_flight_id = Column(Integer(unsigned=True), ForeignKey("flights.id"), nullable=False)
    return_flight_id = Column(Integer(unsigned=True), ForeignKey("flights.id"), nullable=True)
    ticket_class_id = Column(Integer(unsigned=True), ForeignKey("ticket_classes.id"), nullable=False)
    count_adult = Column(Integer, nullable=False,default=1)
    count_child = Column(Integer, nullable=False,default=0)
    count_infant = Column(Integer, nullable=False,defailt=0)
    item_amount = Column(Numeric(10, 2), nullable=False)

    booking = relationship("Booking", back_populates="booking_items")

