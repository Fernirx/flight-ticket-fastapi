from sqlalchemy import Column, ForeignKey,Enum,Numeric
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship
from app.config.database import Base


class BookingItem(Base):
    __tablename__ = "booking_items"

    id = Column(INTEGER(unsigned=True), primary_key=True, index=True)
    booking_id = Column(INTEGER(unsigned=True), ForeignKey("bookings.id"), nullable=False)
    trip_type = Column(Enum("one way", "round trip"), nullable=False)
    departure_flight_id = Column(INTEGER(unsigned=True), ForeignKey("flights.id"), nullable=False)
    return_flight_id = Column(INTEGER(unsigned=True), ForeignKey("flights.id"), nullable=True)
    ticket_class_id = Column(INTEGER(unsigned=True), ForeignKey("ticket_classes.id"), nullable=False)
    count_adult = Column(INTEGER, nullable=False,default=1)
    count_child = Column(INTEGER, nullable=False,default=0)
    count_infant = Column(INTEGER, nullable=False,defailt=0)
    item_amount = Column(Numeric(10, 2), nullable=False)

    booking = relationship("Booking", back_populates="booking_items")

