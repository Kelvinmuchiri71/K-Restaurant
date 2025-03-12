#!/home/k/.pyenv/shims/python

from sqlalchemy import Column, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship
from .base import Base

#Many-to-Many Association Table
order_items = Table(
    "order_items", Base.metadata,
    Column("order_id", Integer, ForeignKey("order.id"), primary_key=True),
    Column("menu_id", Integer, ForeignKey("menu_items.id"), primary_key=True)

)

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))

    customer = relationship("Customer", back_populates="orders")
    menu_items = relationship("Menu", secondary="order_items", back_populates="orders")

    