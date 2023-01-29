from typing import Union

from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi_jwt_auth import AuthJWT
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

@app.get("/protected")
def protected_contents(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    return current_user


@app.on_event("startup")
def init_app():
    create_db_and_tables()

# add errorHandler with custom errors
app.add_middleware(HttpRequestMiddleware)