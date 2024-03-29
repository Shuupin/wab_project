from fastapi import APIRouter, Depends
from .mqqt import publish
from .schemas import Item, IdSchema, ItemUpdate
from .database import get_db
from fastapi import Request
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
import json
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from . import auth , models
item_routes = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
@item_routes.post("/create-item")
async def create_item(item:Item,token: Annotated[models.User, Depends(oauth2_scheme)]):
    json_string = jsonable_encoder(item)
    json_string["method"]="Insert"
    json_string["table"]="Item"
    # print(json_string["table"])   
    publish(json.dumps(json_string)) 

@item_routes.post("/update-item")
async def update_warehouse(item:ItemUpdate,token: Annotated[models.User, Depends(oauth2_scheme)]):
    json_string = jsonable_encoder(item)
    json_string["method"]="Update"
    json_string["table"]="Item"
    # print(json_string["table"])   
    publish(json.dumps(json_string)) 
   
@item_routes.post("/delete-item")
async def delete_warehouse(id:IdSchema,token: Annotated[models.User, Depends(oauth2_scheme)]):
    json_string = jsonable_encoder(id)
    json_string["method"]="Delete"
    json_string["table"]="Item"
    # print(json_string["table"])   
    publish(json.dumps(json_string)) 