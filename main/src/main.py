from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from .routes import auth 
from dotenv import load_dotenv
import os

load_dotenv()
app = FastAPI()

from starlette.middleware.sessions import SessionMiddleware
app.add_middleware(SessionMiddleware, secret_key=os.environ.get("MIDDLEWARE_KEY"))

app.include_router(auth.auth_routes)


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
