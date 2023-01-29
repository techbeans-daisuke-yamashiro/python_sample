from datetime import datetime
from pprint import pprint
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
from errors import ApiException,extract_errors
from services.authorization import UserLogin,UserLoginResponse,HashedPassword

#Generate Custom Responce in this controller
UserLoginError = ApiException(status_code=401, message='Login Failed')
successful = {200:{'description': 'Login successfully'}}
login_user_responces = extract_errors([UserLoginError])
login_user_responces.update(successful)

LoginRouter = APIRouter(
    prefix="/login",
    tags=["login"]
)

@LoginRouter.post('/',response_model=UserLoginResponse
    , responses=login_user_responces)
def login(user:UserLogin, Authorize:AuthJWT=Depends(),
    session: Session=Depends(get_session)):
    u = session.exec(
        select(User).where(User.name==user.name)).first()
    pprint(f'recived user {user.name}/{user.password}')
    pprint(f'Got user={u}')
    if (u is not None) and HashedPassword.verify(user.password, u.password):
        print('password valid.')
        identity ={
            'user_id': u.id,
            'user_name': u.name,
        }
        user_login_response = UserLoginResponse(
            access_token = Authorize.create_access_token(subject=u.email),
            refresh_token = Authorize.create_refresh_token(subject=u.email))
        #user_login_response.refresh_token = Authorize.create_refresh_token()
        return user_login_response
    elif(u is None):
        raise UserLoginError
    elif(u['password'] == user.password):
       raise UserLoginError
