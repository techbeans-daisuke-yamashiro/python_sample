from datetime import datetime
from typing import List,Optional
from database import get_session
from database.models import User, UserUpdate, UserCreate, UserRead
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response, ORJSONResponse
from fastapi_jwt_auth import AuthJWT
#from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlmodel import Session, select
from database import get_session
from errors import ApiException
from services.authorization import UserLogin,UserLoginResponse,HashedPassword


LoginRouter = APIRouter(
    prefix="/login",
    tags=["login"]
)

@LoginRouter.post('/',response_model=UserLoginResponse
    , responses=error_response([InvalidPasswordError,UserNotFoundError]))
def login(user:UserLogin, Authorize:AuthJWT=Depends(),
    session: Session=Depends(get_session)):
    validate_user = session.exec(
        select(User).where(User.email==user.email)).first()
    if (validate_user is not None) and HashedPassword.verify(user.password, validate_user.password):
        identity ={
            'user_id': user.id,
            'user_name': user.name,
        }
        user_login_response = UserLoginResponse()
        user_login_response.access_token = Authorize.create_access_token(
            identity=identity)
        user_login_response.refresh_token = Authorize.create_refresh_token()
        return {'access_token':access_token}
    elif(validate_user is None):
        raise ApiException(status_code=404,message='invalid Email')
    elif(validate_user['password'] == user.password):
       raise ApiException(status_code=401,message='invalid Password')