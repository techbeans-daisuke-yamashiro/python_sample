from typing import List
#from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from fastapi_jwt_auth import AuthJWT

from config import SECRET_KEY,ACCESS_TOKEN_EXPIRES_IN,REFRESH_TOKEN_EXPIRES_IN
from errors import ApiException
from passlib.context import CryptContext

hash_password_context = CryptContext(schemes=["bcrypt"],deprecated="auto")
ALGORITHM = "HS256"

class HashedPassword():
    @staticmethod
    def verify(plain:str, hashed:str):
        return hash_password_context.verify(plain, hashed)

    @staticmethod
    def get(plain:str):
        return hash_password_context.hash(plain)

class UserLogin(BaseModel):
    name: str
    password: str 

    class Config:
        shema_extra={
            'example':{
                'name': 'name',
                'password': 'password'
            }
        }

class Settings(BaseModel):
    authjwt_secret_key: str = str(SECRET_KEY)
    authjwt_access_token_expires: int = ACCESS_TOKEN_EXPIRES_IN
    authjwt_refresh_token_expires: int = REFRESH_TOKEN_EXPIRES_IN

class UserLoginResponse(BaseModel):
    access_token: str
    refresh_token: str

@AuthJWT.load_config
def get_config():
    return Settings()

MissingTokenError = ApiException(status_code=401, message='You are not logged in')
UserNotFoundError = ApiException(status_code=401, message='User no longer exist')
NotVerifiedError = ApiException(status_code=401, message='Please verify your account')
TokenExpiredError = ApiException(status_code=401, message='Token is invalid or has expired')

def dispatch_jwt_authrization_error(e : Exception):
    error = e.__class__.__name__
    if error == 'MissingTokenError':
        raise MissingTokenError
    if error == 'UserNotFound':
        raise UserNotFoundError
    if error == 'NotVerified':
        raise NotVerifiedError
    raise TokenExpiredError
