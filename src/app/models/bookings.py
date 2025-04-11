from sqlalchemy import Column, ForeignKey, DateTime, Numeric,Enum,func
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship
from app.config.database import Base

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(INTEGER(unsigned=True), primary_key=True, index=True,autoincrement=True)
    user_id = Column(INTEGER(unsigned=True), ForeignKey("users.id"), nullable=False)
    booking_date = Column(DateTime, nullable=False,server_default=func.now())
    total_amount = Column(Numeric(10, 2), nullable=False)
    status = Column(Enum("Pending", "Confirmed", "Cancelled"), nullable=False, default="Pending")

    user = relationship("User", back_populates="bookings")
    booking_items = relationship("BookingItem", back_populates="booking")