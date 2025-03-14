#!/home/k/.pyenv/shims/python

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.base import Base


DATABASE_URL = "sqlite:///restaurant.db"


engine = create_engine(DATABASE_URL, echo=True)


Session = sessionmaker(bind=engine)

def init_db():
    
    Base.metadata.create_all(bind=engine)


session = Session()
