#!/home/k/.pyenv/shims/python

from sqlalchemy import Column, Integer, ForeignKey, Table, String
from sqlalchemy.orm import relationship
from app.base import Base
from app.menu import Menu

#Many-to-Many Association Table
order_items = Table(
    "order_items", Base.metadata,
    Column("order_id", Integer, ForeignKey("orders.id"), primary_key=True),
    Column("menu_id", Integer, ForeignKey("menu_items.id"), primary_key=True)

)

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    status = Column(String, default="Waiting, Order")

    customer = relationship("Customer", back_populates="orders")
    menu_items = relationship("Menu", secondary="order_items", back_populates="orders")

    @property
    def total_amount(self):
        return sum(item.price for item in self.menu_items)
    
    def __repr__(self):
        return f"<Order {self.id}: {self.customer.name} - Total: KES {self.total_amount}>"
    