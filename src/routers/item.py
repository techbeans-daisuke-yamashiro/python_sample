from datetime import datetime
from typing import List,Optional
from database.models import Item, ItemUpdate, ItemCreate, ItemRead
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response, ORJSONResponse
#from fastapi.encoders import jsonable_encoder
from sqlmodel import Session, select
from database import get_session
from errors import ItemNotFoundError, error_response
ItemRouter = APIRouter(
    prefix="/item",
    tags=["item"]
)


@ItemRouter.get('/{id}/get', response_model=ItemRead)
def select_item(id: int, session: Session = Depends(get_session)):
    data = session.get(Item, id)
    
    if not data:
        raise ItemNotFoundError
    # soft-delete
    if data.deleted_at is not None:
        data = None
    return data


@ItemRouter.get('/all', response_model=List[ItemRead])
def select_all_items(session: Session = Depends(get_session)):
    # soft-delete query
    data = session.exec(select(Item).where(Item.deleted_at is None)).all()
    if not data:
        raise ItemNotFoundError
    return data


@ItemRouter.patch('/update', response_model=ItemUpdate,
    responses={ 200: {'description': 'operation done successfully'}, 
    404: {'description': 'Target item Not Found'}})

def update_item(item: ItemUpdate, session: Session = Depends(get_session)):
    target_item = session.get(Item, item.id)
    if not target_item:
        raise HTTPException(status_code=404, detail="Target item not found")
    item_data = item.dict(exclude_unset=True)
    for key, value in item_data.items():
        setattr(target_item, key, value)
    session.add(target_item)
    session.commit()
    session.refresh(target_item)
    return target_item


@ItemRouter.put('/create', response_model=ItemCreate)
def create_item(item: ItemCreate, session: Session = Depends(get_session)):
    target_item = Item.from_orm(item)
    session.add(target_item)
    session.commit()
    session.refresh(target_item)
    return target_item

#hard delete endppoint
@ItemRouter.delete('/{id}/delete', response_class=ORJSONResponse,
    responses={200:{'description': 'operation done successfully'}, 
    404:{'description': 'Item Not Found'} })
def hard_delete_item(id: int, session: Session = Depends(get_session)):
    target_item = session.get(Item, id)
    if not target_item:
        raise ItemNotFoundError
    session.delete(target_item)
    session.commit()
    return ORJSONResponse(content={'message': 'operation done.'})

@ItemRouter.post('/{id}/delete', response_class=ORJSONResponse,
    responses=error_response([ItemNotFoundError]))
def soft_delete_item(id: int, session: Session = Depends(get_session)):
    target_item = session.get(Item, id)
    if not target_item:
        raise ItemNotFoundError
    target_item.deleted_at = datetime.utcnow()
    session.add(target_item)
    session.commit()
    return ORJSONResponse(content={'message': 'operation done.'})
