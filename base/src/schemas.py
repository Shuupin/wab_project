from pydantic import BaseModel
from uuid import UUID

class User(BaseModel):
    name: str
    surname:str
    position:str
    salary:float
    password:str
    login:str

class UpdateUser(BaseModel):
    uuid:UUID
    name: str
    surname:str
    position:str
    salary:float
class Warehouse(BaseModel):
    address:str
    manager_id:UUID

class WarehouseUpdate(BaseModel):
    address:str
    uuid:UUID
    manager_id:UUID

class Item(BaseModel):
    name:str
    amount:int
    description:str
    warehouse_id:UUID

class ItemUpdate(BaseModel):
    uuid:UUID
    name:str
    amount:int
    description:str
    warehouse_id:UUID

class LoginSchema(BaseModel):
    login:str
    password:str

class IdSchema(BaseModel):
    uuid:UUID
    