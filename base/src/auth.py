from fastapi import APIRouter, status
from dotenv import load_dotenv
from fastapi import Request ,Depends, HTTPException
from os import environ
from . import database , models,schemas
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from typing import Annotated
import hashlib
import jwt
import datetime
import uuid
load_dotenv()

config_data = {
    'GOOGLE_CLIENT_ID': environ.get("GOOGLE_CLIENT_ID"), 
    'GOOGLE_CLIENT_SECRET':environ.get("GOOGLE_CLIENT_SECRET") 
}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
auth_routes = APIRouter()

from starlette.config import Config
starlette_config = Config(environ=config_data)

from authlib.integrations.starlette_client import OAuth
oauth = OAuth(starlette_config)
oauth.register(
    name="google",
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'},
)



# @auth_routes.get('/auth/oauth-login')
# async def login(request: Request):
#     return await oauth.google.authorize_redirect(request, "http://localhost:8000/oauth-token")

# from authlib.integrations.starlette_client import OAuthError
# import logging

# @auth_routes.get('/oauth-token')
# async def token(request: Request):
#     # try:
#     access_token = await oauth.google.authorize_access_token(request)
#     # except OAuthError:
#     #   raise ...
#     return access_token['id_token']

@auth_routes.post('/login')
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    db = database.get_db()
    user = db.query(models.User).filter((models.User.email == form_data.username) and (models.User.password == hashlib.sha256(form_data.password).hexdigest())).first()
    if user:
        token = jwt.encode({
            "iss":str(user.id),
            "exp":int((datetime.datetime.now() + datetime.timedelta(hours=2)).timestamp()),
        },
        environ.get("JWT_SECRET"),
          algorithm='HS256')
        
        return {"access_token": token, "token_type": "bearer"}
        #generate token
    else:
        raise HTTPException(status_code=401,detail="Password or login are incorect")
    



async def get_current_user(token: Annotated[any, Depends(oauth2_scheme)]):
    print(token)
    user_id = jwt.decode(token["access_token"],environ.get("JWT_SECRET"),algorithms=["HS256"])
    db = database.get_db()
    user = db.query(models.User).filter(models.User.id == uuid.UUID(user_id).hex).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


