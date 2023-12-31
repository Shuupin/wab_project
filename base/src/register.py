from fastapi import APIRouter, Depends
from .mqqt import publish
from .schemas import User
from . import models
from .database import get_db
from fastapi import Request , HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
import json
import hashlib
registration_routes = APIRouter()


@registration_routes.post("/register-user")
async def register_user(user:User):
    db = get_db()
    user_db = db.query(models.User).filter((models.User.email == user.login)).first()
    if user_db:
        raise HTTPException(status_code=401,detail="User already exists")
    else:
        json_string = jsonable_encoder(user)
        json_string["method"]="Insert"
        json_string["table"]="User"
        json_string["password"] =  hashlib.sha256(json_string["password"].encode('utf-8')).hexdigest()
        # print(json_string["table"])   
        publish(json.dumps(json_string)) 
