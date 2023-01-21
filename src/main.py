from typing import Union

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from database import create_db_and_tables,create_seed_data

#initialize FastAPI
app = FastAPI()
app.mount("/assets", StaticFiles(directory="assets"), name="static")

@app.get("/")
def read_root():
    return {"Hello": "World!"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.on_event("startup")
def init_app():
    create_db_and_tables()
    create_seed_data()

if __name__ == '__main__':
    init_app()
