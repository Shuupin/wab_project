from fastapi import APIRouter
from dotenv import load_dotenv
from fastapi import Request
from os import environ

load_dotenv()

config_data = {
    'GOOGLE_CLIENT_ID': environ.get("GOOGLE_CLIENT_ID"), 
    'GOOGLE_CLIENT_SECRET':environ.get("GOOGLE_CLIENT_SECRET") 
}

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



@auth_routes.get('/auth/oauth-login')
async def login(request: Request):
    return await oauth.google.authorize_redirect(request, "http://localhost:8000/oauth-token")

from authlib.integrations.starlette_client import OAuthError
import logging

@auth_routes.get('/oauth-token')
async def token(request: Request):
    # try:
    access_token = await oauth.google.authorize_access_token(request)
    # except OAuthError:
    #   raise ...
    return access_token['id_token']