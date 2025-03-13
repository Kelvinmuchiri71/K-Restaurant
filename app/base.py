#!/home/k/.pyenv/shims/python

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


my_engine = create_engine("sqlite:///restaurant.db" , echo=True)
Session = sessionmaker(bind=my_engine)
session = Session()

Base = declarative_base()

