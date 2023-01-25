# entrypoint for '/api'
from .item import ItemRouter
from fastapi import APIRouter

APIRoot = APIRouter(prefix='/api')

#connect itemRouter as Sub directory
APIRoot.include_router(ItemRouter)