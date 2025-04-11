from sqlalchemy import Column, ForeignKey, Enum, Numeric, DateTime,func
from sqlalchemy.dialects.mysql import INTEGER
from app.config.database import Base

class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(INTEGER(unsigned=True), primary_key=True, index=True,autoincrement=True)
    cart_id = Column(INTEGER(unsigned=True), ForeignKey("shopping_carts.id"), nullable=False)
    trip_type = Column(Enum("one way","round trip"), nullable=False)
    departure_flight_id = Column(INTEGER(unsigned=True), ForeignKey("flights.id"), nullable=False)
    return_flight_id = Column(INTEGER(unsigned=True), ForeignKey("flights.id"), nullable=True)
    ticket_class_id = Column(INTEGER(unsigned=True), ForeignKey("ticket_classes.id"), nullable=False)
    count_adult = Column(INTEGER, nullable=False,default=1)
    count_child = Column(INTEGER, nullable=False,default=0)
    count_infant = Column(INTEGER, nullable=False,default=0)
    price = Column(Numeric(10,2), nullable=False)
    created_at = Column(DateTime, nullable=False,server_default=func.now())
    updated_at = Column(DateTime, nullable=False,server_default=func.now())