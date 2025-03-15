#!/home/k/.pyenv/shims/python

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.base import Base


class Customer(Base):
    __tablename__ = "customers"


    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    phone = Column(String, unique=True, nullable=False)

    orders = relationship("Order",  back_populates="customer")


    def __repr__(self):
        return f"<Customer {self.name} - {self.phone}>"
    