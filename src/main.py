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

# sample of JWT protected endpoint
#  protected by Authorize.jwt_required()
@app.get("/protected")
def protected_contents(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    return current_user

# sample of JWT protected(optional) endpoint
#  protected by Authorize.jwt_optional()
@app.get("/optional")
def optional_protected_contents(Authorize: AuthJWT = Depends()):
    res = {"message": "not logged in"}
    Authorize.jwt_optional()
    current_user = Authorize.get_jwt_subject()
    if current_user:
        res = {
            "message":f"logged in {current_user}"
        }
    return res

@app.on_event("startup")
def init_app():
    create_db_and_tables()

# add errorHandler with custom errors
app.add_middleware(HttpRequestMiddleware)