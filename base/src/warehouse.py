from fastapi import APIRouter, Depends
from .mqqt import publish
from .schemas import Warehouse, IdSchema,WarehouseUpdate
from .database import get_db
from fastapi import Request
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
import json
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from . import auth , models
warehouse_routes = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
@warehouse_routes.post("/create-warehouse")
async def create_warehouse(warehouse:Warehouse,token: Annotated[models.User, Depends(oauth2_scheme)]):
    json_string = jsonable_encoder(warehouse)
    json_string["method"]="Insert"
    json_string["table"]="Warehouse"
    # print(json_string["table"])   
    publish(json.dumps(json_string)) 

@warehouse_routes.post("/update-warehouse")
async def update_warehouse(warehouse:WarehouseUpdate,token: Annotated[models.User, Depends(oauth2_scheme)]):
    json_string = jsonable_encoder(warehouse)
    json_string["method"]="Update"
    json_string["table"]="Warehouse"
    # print(json_string["table"])   
    publish(json.dumps(json_string)) 
   
@warehouse_routes.post("/delete-warehouse")
async def delete_warehouse(warehouse:IdSchema,token: Annotated[models.User, Depends(oauth2_scheme)]):
    json_string = jsonable_encoder(warehouse)
    json_string["method"]="Delete"
    json_string["table"]="Warehouse"
    # print(json_string["table"])   
    publish(json.dumps(json_string)) 