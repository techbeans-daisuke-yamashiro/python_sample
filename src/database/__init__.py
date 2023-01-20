#Databse Handler
from config import DATABASE_URL
from .models import Item,User

from typing import Optional
from sqlmodel import SQLModel, Session, create_engine


#Connecting to Database
engine = create_engine(DATABASE_URL,echo=True) 

def get_session():
    with Session(engine) as session:
        yield session

#Create DB and tables
def create_db_and_tables():
    SQLModel.metadata.create_all(engine) 

def create_seed_data():
    users = [
        User(name="Alice",   email="alice@example.com"),
        User(name="Jack",    email="jack@example.com"),
        User(name="Takashi", email="takashi@example.com"),
    ]
    items =[
        Item(name="Apple",  price=10, country='JP'),
        Item(name="Orange", price=15, country='ES'),
        Item(name="Banana", price=30, country='PH'),
        Item(name="Mango",  price=35, country='TH'),
        Item(name="Grape",  price=25, country='JP'),
    ]
    with Session(engine) as session:
        for user in users:
            session.add(user)
        for item in items:
            session.add(item)
        session.commit()