
from fastapi import APIRouter, Depends
from .mqqt import publish
from .schemas import UpdateUser, IdSchema
from .database import get_db
from fastapi import Request
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
import json
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from . import auth , models
user_routes = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

@user_routes.post("/update-user")
async def update_warehouse(user:UpdateUser,token: Annotated[models.User, Depends(oauth2_scheme)]):
    json_string = jsonable_encoder(user)
    json_string["method"]="Update"
    json_string["table"]="User"
    # print(json_string["table"])   
    publish(json.dumps(json_string)) 
   
@user_routes.post("/delete-user")
async def delete_warehouse(id:IdSchema,token: Annotated[models.User, Depends(oauth2_scheme)]):
    json_string = jsonable_encoder(id)
    json_string["method"]="Delete"
    json_string["table"]="User"
    # print(json_string["table"])   
    publish(json.dumps(json_string)) 