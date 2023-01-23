from typing import Union

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from database import create_db_and_tables, create_seed_data

from routers.item import ItemRouter

#initialize FastAPI
app = FastAPI()
app.mount("/assets", StaticFiles(directory="assets"), name="static")
app.include_router(ItemRouter)

@app.get("/")
def read_root():
    return {"Hello": "World!"}


@app.on_event("startup")
def init_app():
    pass
