from pydantic import BaseModel


class User(BaseModel):
    name: str
    surname:str
    position:str
    salary:float


class Warehouse:
    address:str
    area:float
    manager:User

class Item(BaseModel):
    name:str
    amount:int
    warehouse:Warehouse
