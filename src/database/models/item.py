from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel, select, Session
from sqlalchemy import func

# Item model
##Base model
class ItemBase(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str] = Field(index=True)
    price: Optional[int] = Field(default=None,nullable=False)
    country: Optional[str] = Field(index=True,nullable=True)
    created_at: Optional[datetime] = Field(default=datetime.utcnow(),nullable=False)
    updated_at: Optional[datetime] = Field(default=datetime.utcnow(),
        sa_column_kwargs={'onupdate': datetime.now},
        nullable=False)
    deleted_at: Optional[datetime] = Field(nullable=True)
    seeded:  bool = Field(default=False)


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

    @classmethod
    def select_all(self, engine):
        with Session(engine) as session:
            statement = select(self)
            data = session.exec(statement).all()
        return data

    @classmethod
    def get_count_seeded(self,engine):
        session=Session(engine)
        return session.query(self).where(self.seeded==True).count()
         