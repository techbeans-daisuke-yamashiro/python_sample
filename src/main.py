from typing import Union

from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi_jwt_auth import AuthJWT
from database import create_db_and_tables, create_seed_data
from errors import HttpRequestMiddleware
from services.authorization import dispatch_jwt_authrization_error
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

# sample of JWT protected endpoint
# protected by Authorize.jwt_required() 
# dispatch Authrization Exception with dispatch_jwt_authrization_error() 
@app.get("/protected")
def protected_contents(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        dispatch_jwt_authrization_error(e)
    current_user = Authorize.get_jwt_subject()
    return current_user

@app.on_event("startup")
def init_app():
    create_db_and_tables()

# add errorHandler with custom errors
# if DEBUG=True in .env
if not DEBUG:
    app.add_middleware(HttpRequestMiddleware)