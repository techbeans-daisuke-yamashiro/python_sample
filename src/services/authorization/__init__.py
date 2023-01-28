from typing import List
#from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from fastapi_jwt_auth import AuthJWT

from config import SECRET_KEY,ACCESS_TOKEN_EXPIRES_IN,REFRESH_TOKEN_EXPIRES_IN
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
    email: str
    password: str 

    class Config:
        shema_extra={
            'example':{
                'email': 'user@example.com',
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