from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from fastapi_jwt_auth import AuthJWT

from config import SECRET_KEY
from passlib.context import CryptContext

hash_password_context = CryptContext(schemes=["bcrypt"],deprecated="auto")
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 7 days
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
    auth_jwt_key: str = "56c2067bf62d2b98d9741466d877e95a3341a846b05c08909a9b915b1229f859"

class UserLoginResponse(BaseModel):
    access_token: str

@AuthJWT.load_config
def get_config():
    return Settings()