from sqlalchemy import Boolean, Column, ForeignKey, UUID, Integer, String
from sqlalchemy.orm import relationship

from database import Base

class User(Base):
    __tablename__ = "user"
    id = Column(UUID,primary_key = True,index = True)
    name = Column(String(50),nullable = False, index = True)
    surname = Column(String(50),nullable = False)
    salary = Column(Integer,nullable = False,index = True)
    email = Column(String(50),nullable = False,index = True)
    password = Column(String(1000),nullable = False)
    position = Column(String(50),nullable = False)

class Warehouse(Base):
    __tablename__="warehouse"
    id = Column(UUID,primary_key = True, index =True)
    address = Column(String(500),nullable = False,index = True)
    manager_id = Column(UUID,ForeignKey('user.id'),nullable = False,index =True)
    
    warehouse = relationship(User)



class Item(Base):
    __tablename__ = "item"

    id = Column(UUID, primary_key=True, index=True)
    name = Column(String(1000),index = True,nullable = False)
    amount = Column(Integer,nullable=False,index = True)
    warehouse_id = Column(UUID,ForeignKey('warehouse.id'),nullable = False)
    description = Column(String(500),nullable = False)

    warehouse = relationship(Warehouse)