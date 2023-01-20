from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel, select, Session

# Item model
##Base model
class ItemBase(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    price: int = Field(default=None)
    country: str = Field(index=True)
    created_at: datetime = Field(default=datetime.utcnow(),nullable=False)
    updated_at: datetime = Field(default_factory=datetime.
        utcnow,nullable=False)


##Table Model
class Item(ItemBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    #Sample classmethod
    @classmethod
    def select_by_id(self, engine, id):
        with Session(engine) as session:
            statement = select(self).where(self.id == id)
            data = session.exec(statement).first()
        return data

    @classmethod
    def select_by_country(self, engine, country):
        with Session(engine) as session:
            statement = select(self).where(self.country == country)
            data = session.exec(statement).all()
        return data

class ItemCreate(ItemBase):
    pass

class ItemRead(ItemBase):
    id: int

class ItemUpdate(ItemBase):
    id: Optional[int] = None
    name: Optional[str] = None
    price: Optional[int] = None

# User model
##Base model
class UserBase(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    email: str = Field(index=True)
    created_at: datetime = Field(default=datetime.utcnow(),nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow,
        nullable=False)

##Table Model
class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    #Sample classmethod
    @classmethod
    def select_by_id(self, engine, id):
        with Session(engine) as session:
            statement = select(self).where(self.id == id)
            data = session.exec(statement).first()
        return data

class UserCreate(UserBase):
    pass

class UserRead(UserBase):
    id: int

class UserUpdate(UserBase):
    id: Optional[int] = None
    name: Optional[str] = None
    email: Optional[str] = None