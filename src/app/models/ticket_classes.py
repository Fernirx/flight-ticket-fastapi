from sqlalchemy import Column, Integer,Enum,Numeric
from app.config.database import Base

class ShoppingCart(Base):
    __tablename__ = "ticket_classes"

    id = Column(Integer(unsigned=True), primary_key=True, index=True,autoincrement=True,nullable=False)
    class_name = Column(Enum("Economy","Premium Economy","Business"),nullable=False)
    price_multiplier=Numeric(5,2),default=1,nullable=False