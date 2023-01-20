from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel, select, Session

# User model
##Base model
class UserBase(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    email: str = Field(index=True)
    created_at: datetime = Field(default=datetime.utcnow(),nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow,
        nullable=False)

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
    id: Optional[int] = Field(default=None, primary_key=True)

    #Sample classmethod
    @classmethod
    def select_by_id(self, engine, id):
        with Session(engine) as session:
            statement = select(self).where(self.id == id)
            data = session.exec(statement).first()
        return data
