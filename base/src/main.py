from fastapi import  FastAPI , Depends
from fastapi.responses import HTMLResponse
from .auth import auth_routes
from .warehouse import warehouse_routes
from .item import item_routes
from .register import registration_routes 
from .user import user_routes
from dotenv import load_dotenv
import os
from fastapi.security import OAuth2PasswordBearer
from .database import SessionLocal, engine
from . import models

from typing import Annotated


load_dotenv()
app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

models.Base.metadata.create_all(bind=engine)

from starlette.middleware.sessions import SessionMiddleware
app.add_middleware(SessionMiddleware, secret_key=os.environ.get("MIDDLEWARE_KEY"))

app.include_router(registration_routes)
app.include_router(auth_routes)
app.include_router(warehouse_routes)
app.include_router(item_routes)
app.include_router(user_routes)

@app.get('/')
async def root():
    return HTMLResponse('''
<body>
    <a href="/auth/oauth-login">Log In</a>
</body>''')

#@app.get('/token')
#async def token(request: Request):
#    return request.headers

# OAuth settings

# Set up OAuth
