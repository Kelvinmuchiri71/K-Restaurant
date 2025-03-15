#!/home/k/.pyenv/shims/python

from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from app.base import Base

class Menu(Base):
    __tablename__ = "menu_items"

    id = Column (Integer, primary_key=True)
    name = Column (String, nullable=False)
    price = Column (Float, nullable=False)
    category = Column (String, nullable=False)

    orders = relationship("Order", secondary="order_items", back_populates="menu_items")

    def __repr__(self):
        return f"<Menu {self.name} - KES {self.price}>"
