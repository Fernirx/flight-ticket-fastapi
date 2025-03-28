from sqlalchemy import Column, Integer, ForeignKey, DateTime, Float, String
from sqlalchemy.orm import relationship
from app.config.database import Base

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    booking_date = Column(DateTime, nullable=False)
    total_amount = Column(Float, nullable=False)
    status = Column(String(50), nullable=False)

    user = relationship("User", back_populates="bookings")
    booking_items = relationship("BookingItem", back_populates="booking")