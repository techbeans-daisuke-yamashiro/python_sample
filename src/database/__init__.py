#Databse Handler
from config import DATABASE_URL,DB_ECHO
from .models import Item, User

from typing import Optional
from sqlmodel import SQLModel, Session, create_engine
from starlette.requests import Request

#Connecting to Database
engine = create_engine(DATABASE_URL, echo=DB_ECHO) 

def get_connection(request: Request):
    return request.state.connection
    
def get_session():
    with Session(engine) as session:
        yield session

#Create DB and tables
def create_db_and_tables():
    SQLModel.metadata.create_all(engine) 

#Create Seed Data
def create_seed_data():
    seeding = False
    users = None
    items = None
    if (User.get_count_seeded(engine) + Item.get_count_seeded(engine)) is 0:
        seeding=True
        users = [
            User(name="Alice",   email="alice@example.com",seeded=True),
            User(name="Jack",    email="jack@example.com",seeded=True),
            User(name="Takashi", email="takashi@example.com",seeded=True),
        ]
        items =[
            Item(name="Apple",  price=10, country='JP',seeded=True),
            Item(name="Orange", price=15, country='ES',seeded=True),
            Item(name="Banana", price=30, country='PH',seeded=True),
            Item(name="Mango",  price=35, country='TH',seeded=True),
            Item(name="Grape",  price=25, country='JP',seeded=True),
        ]
    
    with Session(engine) as session:
        if users is not None:
            print("seeding table \'user\'")
            for user in users:
                session.add(user)
        else:
            print("skipped seeding table \'user\'")
        if items is not None:
            print("seeding table \'item\'")
            for item in items:
                session.add(item)
        else:
            print("skipped seeding table \'item\'")
        session.commit()