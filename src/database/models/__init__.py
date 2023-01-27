#__init__.py:
# Model package entrypoint
#add models like:
#from .modulename import TableModelName
from datetime import datetime
from typing import Optional,Union
from sqlmodel import Field, SQLModel

# User model
##Base model
class UserBase(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field()
    email: str = Field()
    password: str = Field()
    created_at: Optional[datetime] = Field(default=datetime.utcnow(),nullable=False)
    updated_at: Optional[datetime] = Field(default=datetime.utcnow(),
        sa_column_kwargs={'onupdate': datetime.now},
        nullable=False)
    deleted_at: Optional[datetime] = Field(nullable=True)
    seeded:  bool = Field(default=False)

class UserCreate(UserBase):
    pass

class UserRead(UserBase):
    id: int

class UserUpdate(UserBase):
    id: Optional[int] = None
    name: Optional[str] = None
    email: Optional[str] = None

##Table Model
class User(UserBase, table=True):
    __table_args__ = {'extend_existing': True}
    id: Optional[int] = Field(default=None, primary_key=True)


# Item model
##Base model
class ItemBase(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str] = Field(index=True)
    price: Optional[int] = Field(default=None,nullable=False)
    country: Optional[str] = Field(index=True,nullable=True)
    created_at: Optional[datetime] = Field(default=datetime.utcnow(),
        nullable=False)
    updated_at: Optional[datetime] = Field(default=datetime.utcnow(),
        sa_column_kwargs={'onupdate': datetime.now},
        nullable=False)
    deleted_at: Optional[datetime] = Field(nullable=True)
    seeded:  bool = Field(default=False)


class ItemCreate(ItemBase):
    id: Union[int, None] = None
    created_at: Union[datetime, None] = None
    updated_at: Union[datetime, None] = None
    deleted_at: Union[datetime, None] = None
    seeded: Union[bool, None] = None
 
class ItemRead(ItemBase):
    id: int

class ItemUpdate(ItemBase):
    id: Optional[int] = Field()
    name: Optional[str] = Field()
    price: Optional[int] = Field()
    country: Optional[str] = Field()

##Table Model
class Item(ItemBase, table=True):
    __table_args__ = {'extend_existing': True}
    id: Optional[int] = Field(default=None, primary_key=True)

#event listener for soft deleting
"""
Queryを利用するController側から'WHERE deleted_at NOT NULL'でフィルタするように
したほうが建設的、との結論に至ったので
"""