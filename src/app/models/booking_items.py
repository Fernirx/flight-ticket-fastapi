from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.config.database import Base


class BookingItem(Base):
    __tablename__ = "booking_items"

    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey("bookings.id"), nullable=False)
    trip_type = Column(String(50), nullable=False)
    departure_flight_id = Column(Integer, ForeignKey("flights.id"), nullable=False)
    return_flight_id = Column(Integer, ForeignKey("flights.id"), nullable=True)
    ticket_class_id = Column(Integer, ForeignKey("ticket_classes.id"), nullable=False)
    count_adult = Column(Integer, nullable=False)
    count_child = Column(Integer, nullable=False)
    count_infant = Column(Integer, nullable=False)
    item_amount = Column(Float, nullable=False)

    booking = relationship("Booking", back_populates="booking_items")

