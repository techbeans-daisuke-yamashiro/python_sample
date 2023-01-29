from typing import Union

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from database import create_db_and_tables, create_seed_data
from errors import HttpRequestMiddleware
from config import DEBUG

from routers import APIRoot
from routers.login import LoginRouter
#initialize FastAPI
app = FastAPI(debug=DEBUG)
app.mount("/assets", StaticFiles(directory="assets"), name="static")
app.include_router(APIRoot)
app.include_router(LoginRouter)

@app.get("/")
def read_root():
    return {"Hello": "World!"}


@app.on_event("startup")
def init_app():
    create_db_and_tables()

# add errorHandler with custom errors
app.add_middleware(HttpRequestMiddleware)