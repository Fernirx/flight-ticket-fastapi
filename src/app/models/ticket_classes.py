from sqlalchemy import Column,Enum,Numeric
from sqlalchemy.dialects.mysql import INTEGER
from app.config.database import Base

class ShoppingCart(Base):
    __tablename__ = "ticket_classes"

    id = Column(INTEGER(unsigned=True), primary_key=True, index=True,autoincrement=True,nullable=False)
    class_name = Column(Enum("Economy","Premium Economy","Business"),nullable=False)
    price_multiplier=Column(Numeric(5,2),default=1,nullable=False)