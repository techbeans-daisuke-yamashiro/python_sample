#__init__.py:
# Model package entrypoint
#add models like:
#from .modulename import TableModelName
from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel, Session
from sqlalchemy import event, orm

# ModelBase
class ModelBase(SQLModel):
    created_at: Optional[datetime] = Field(default=datetime.utcnow(),nullable=False)
    updated_at: Optional[datetime] = Field(default=datetime.utcnow(),
        sa_column_kwargs={'onupdate': datetime.now},
        nullable=False)
    deleted_at: Optional[datetime] = Field(nullable=True)
    seeded:  bool = Field(default=False)
    

# User model
##Base model
class UserBase(ModelBase):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    email: str = Field(index=True)

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
class ItemBase(ModelBase):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str] = Field(index=True)
    price: Optional[int] = Field(default=None,nullable=False)
    country: Optional[str] = Field(index=True,nullable=True)


class ItemCreate(ItemBase):
    pass

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
@event.listens_for(Session, "do_orm_execute")
def _add_filtering_deleted_at(execute_state):
    論理削除用のfilterを自動的に適用する
    以下のようにすると、論理削除済のデータも含めて取得可能
    query(...).filter(...).execution_options(include_deleted=True)
    if (
        execute_state.is_select
        and not execute_state.is_column_load
        and not execute_state.is_relationship_load
        and not execute_state.execution_options.get("include_deleted", False)
    ):
        execute_state.statement = execute_state.statement.options(
            orm.with_loader_criteria(
                ModelBase,
                lambda cls: cls.deleted_at.is_(None),
                include_aliases=True,
            )
        )

"""