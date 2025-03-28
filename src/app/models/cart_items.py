from sqlalchemy import Column, Integer, ForeignKey, String, Float, DateTime
from app.config.database import Base

class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True, index=True)
    cart_id = Column(Integer, ForeignKey("shopping_carts.id"), nullable=False)
    trip_type = Column(String(50), nullable=False)
    departure_flight_id = Column(Integer, ForeignKey("flights.id"), nullable=False)
    return_flight_id = Column(Integer, ForeignKey("flights.id"), nullable=True)
    ticket_class_id = Column(Integer, ForeignKey("ticket_classes.id"), nullable=False)
    count_adult = Column(Integer, nullable=False)
    count_child = Column(Integer, nullable=False)
    count_infant = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)