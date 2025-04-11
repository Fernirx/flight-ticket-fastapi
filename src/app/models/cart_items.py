from sqlalchemy import Column, Integer, ForeignKey, Enum, Numeric, DateTime,func
from app.config.database import Base

class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(Integer(unsigned=True), primary_key=True, index=True,autoincrement=True)
    cart_id = Column(Integer(unsigned=True), ForeignKey("shopping_carts.id"), nullable=False)
    trip_type = Column(Enum("one way","round trip"), nullable=False)
    departure_flight_id = Column(Integer(unsigned=True), ForeignKey("flights.id"), nullable=False)
    return_flight_id = Column(Integer(unsigned=True), ForeignKey("flights.id"), nullable=True)
    ticket_class_id = Column(Integer(unsigned=True), ForeignKey("ticket_classes.id"), nullable=False)
    count_adult = Column(Integer, nullable=False,default=1)
    count_child = Column(Integer, nullable=False,default=0)
    count_infant = Column(Integer, nullable=False,default=0)
    price = Column(Numeric(10,2), nullable=False)
    created_at = Column(DateTime, nullable=False,server_default=func.now())
    updated_at = Column(DateTime, nullable=False,server_default=func.now())