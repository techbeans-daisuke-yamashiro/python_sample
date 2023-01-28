#Databse Handler
from config import DATABASE_URL, DB_ECHO, SECRET_KEY
from .models import Item, User
from services.authorization import HashedPassword
from typing import Optional
from sqlmodel import SQLModel, Session, create_engine,select

#Connecting to Database
engine = create_engine(DATABASE_URL, echo=DB_ECHO) 

def get_session():
    with Session(engine) as session:
        yield session

#Create DB and tables
def create_db_and_tables():
    SQLModel.metadata.create_all(engine) 

#Create Seed Data
def create_seed_data():
    pass
    seeding = False
    session = Session(engine)
    seeded_users = session.exec(select(User).where(User.seeded==True)).all()
    seeded_items = session.exec(select(Item).where(Item.seeded==True)).all()
    if len(seeded_users) == 0:
        users = [
            User(name="Alice",   email="alice@example.com",
                password=HashedPassword.get('password'), seeded=True),
            User(name="Jack",    email="jack@example.com",
                password=HashedPassword.get('password'), seeded=True),
            User(name="Takashi", email="takashi@example.com",
                password=HashedPassword.get('password'), seeded=True),
        ]
        print("seeding table \'user\'")
        for user in users:
            session.add(user)
    else:
        print("skipped seeding table \'user\'")

    if len(seeded_items) == 0:
        items =[
            Item(name="Apple",  price=10, country='JP',seeded=True),
            Item(name="Orange", price=15, country='ES',seeded=True),
            Item(name="Banana", price=30, country='PH',seeded=True),
            Item(name="Mango",  price=35, country='TH',seeded=True),
            Item(name="Grape",  price=25, country='JP',seeded=True),
        ]
        print("seeding table \'Item\'")
        for item in items:
            session.add(item)
    else:
        print("skipped seeding table \'item\'")
    
    session.commit()
