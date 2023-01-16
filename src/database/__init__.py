#Databse Handler
from config import DATABASE_URL
from .models import Item,User

from typing import Optional

#from fastapi import FastAPI, HTTPException, Query
from sqlmodel import SQLModel, Session, create_engine

#Connecting to Database
engine = create_engine(DATABASE_URL,echo=True) 

def get_session():
    with Session(engine) as session:
        yield session

#Create DB and tables;
def create_db_and_tables():
    SQLModel.metadata.create_all(engine) 