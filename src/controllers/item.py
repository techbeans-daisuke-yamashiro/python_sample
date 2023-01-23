from database import engine, Item
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder

ItemRouter = APIRouter()

@ItemRouter.get('/item/{id}')
def select_item(id: int=False):
    return jsonable_encoder(Item.select_by_id(engine, id))

@ItemRouter.get('/items')
def select_all_item():
    return jsonable_encoder(Item.select_all(engine))

