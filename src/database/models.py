from typing import Optional
from sqlmodel import Field, SQLModel

# Item model
##Base model
class ItemBase(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    price: int = Field(default=None)

##Table Model
class Item(ItemBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

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

##Table Model
class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class UserCreate(UserBase):
    pass

class UserRead(UserBase):
    id: int

class UserUpdate(UserBase):
    id: Optional[int] = None
    name: Optional[str] = None
    email: Optional[str] = None
