from pydantic import BaseModel
from uuid import UUID

class User(BaseModel):
    name: str
    surname:str
    position:str
    salary:float
    password:str
    login:str


class Warehouse(BaseModel):
    address:str
    area:float
    manager_id:UUID

class Item(BaseModel):
    name:str
    amount:int
    warehouse_id:UUID

class LoginSchema(BaseModel):
    login:str
    password:str