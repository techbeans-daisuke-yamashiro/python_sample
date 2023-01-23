from typing import Optional,List
from database import engine, Item, get_session
from database.models import ItemUpdate,ItemCreate,ItemRead
from fastapi import APIRouter,Depends
from fastapi.encoders import jsonable_encoder
from sqlmodel import Session,select

ItemRouter = APIRouter(
    prefix="/item",
    tags=["item"]
)

@ItemRouter.get('/{id}/get',response_model=ItemRead)
def select_item(id: int, session: Session = Depends(get_session)):
    data=session.get(Item, id)
    return data

@ItemRouter.get('/all',response_model=List[ItemRead])
def select_all_items(session: Session = Depends(get_session)):
    return  session.exec(select(Item)).all()

@ItemRouter.post('/update',response_model=ItemUpdate)
def update_item(item: ItemUpdate, session: Session = Depends(get_session)):
    target_item = session.get(Item,item.id)
    item_data=item.dict(exclude_unset=True)
    for key, value in item_data.items():
        setattr(target_item,key,value)
    session.add(target_item)
    session.commit()
    session.refresh(target_item)
    return target_item

@ItemRouter.post('/create',response_model=ItemCreate)
def create_item(item: ItemCreate, session: Session = Depends(get_session)):
    target_item=Item.from_orm(item)
    session.add(target_item)
    session.commit()
    session.refresh(target_item)
    return target_item

@ItemRouter.delete('/{id}/delete')
def delete_item(id:int, session: Session = Depends(get_session)):
    target_item = session.get(Item, id,)
    session.delete(target_item)
    session.commit()
    return {'message':'operation done.'}
