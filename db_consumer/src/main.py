import pymongo

# client = pymongo.MongoClient("mongodb://localhost:27017/wab_project")
# print(f"Databases: {client.list_database_names()}")
# db = client.get_database('wab_project')
# print(f"{db.name} collections: {db.list_collection_names()}")
# collection = db.get_collection('rabbit')
# print(f"Open {collection.name}")


import pika
import json
import database
import models
import uuid
from sqlalchemy import update

conn_params = pika.ConnectionParameters(host='127.0.0.1')
conn = pika.BlockingConnection(conn_params)
channel = conn.channel()
channel.queue_declare(queue="wab_project",
                      durable=True)

def on_message_callback(channel, method, properties, body):
    print(f"""
channel:   {channel}
method:    {method}
properties:{properties}
body:      {body}""")
    result = json.loads(body)
    db = database.get_db()
    print(result)
    if(result["table"] == "User"):
        if(result["method"]=="Insert"):
            user = models.User(
                id=uuid.uuid4(),
                name=result["name"],
                surname=result["surname"],
                position=result["position"],
                salary=result["salary"],
                password=result["password"],
                email=result["login"],
                )    
            db.add(user)
            db.commit()
            db.refresh(user)
            return user        
        if(result["method"]=="Update"):
            user_db:models.User = db.query(models.User).filter((models.User.id == result["uuid"])).first()
            print("User Update")
            try:
                user_db.name = result["name"]
                user_db.surname = result["surname"]
                user_db.position = result["position"]
                user_db.salary = result["salary"]
            except Exception as error:
                print(f"### Update could not be preformed: {type(error).__name__} ---- {error}")
            
            db.commit()
            return user_db        
        if(result["method"]=="Delete"):
            user_db:models.User = db.query(models.User).filter((models.User.id == result["uuid"])).first()
            print("Detele user")
            print(user_db.name)
            try:
                db.delete(user_db)
            except Exception as error:
                print(f"### Delete could not be preformed: {type(error).__name__} ---- {error}")
            
            db.commit()
            return user_db        
    if(result["table"] == "Warehouse"):
        if(result["method"]=="Insert"):
            warehouse= models.Warehouse(
                id=uuid.uuid4(),
                address = result["address"],
                manager_id = result["manager_id"],
                # area = result["area"]
                                                )    
            try:
                db.add(warehouse)
            except Exception as error:
                print(f"### Insertion could not be preformed: {type(error).__name__} ---- {error}")
            
            db.commit()
            db.refresh(warehouse)
            return warehouse        
        if(result["method"]=="Update"):
            warehouse_db:models.Warehouse = db.query(models.Warehouse).filter((models.Warehouse.id == result["uuid"])).first()
            print("Update warehouse")
            print(warehouse_db.address)
            try:
               warehouse_db.address = result["address"]
               warehouse_db.manager_id = result["manager_id"]
            except Exception as error:
                print(f"### Update could not be preformed: {type(error).__name__} ---- {error}")
            print(warehouse_db.address)
            
            db.commit()
            return warehouse_db        
        if(result["method"]=="Delete"):
            warehouse_db:models.Warehouse = db.query(models.Warehouse).filter((models.Warehouse.id == result["uuid"])).first()
            print("Detele warehouse")
            print(warehouse_db.address)
            try:
                db.delete(warehouse_db)
            except Exception as error:
                print(f"### Delete could not be preformed: {type(error).__name__} ---- {error}")
            
            db.commit()
            return warehouse_db        
    if(result["table"] == "Item"):
        if(result["method"]=="Insert"):
            item= models.Item(
                id=uuid.uuid4(),
                name = result["name"],
                amount = result["amount"],
                description = result["description"],
                warehouse_id = result["warehouse_id"]
                # area = result["area"]
                                                )    
            try:
                db.add(item)
            except Exception as error:
                print(f"### Insertion could not be preformed: {type(error).__name__} ---- {error}")
            
            db.commit()
            db.refresh(item)
            return item        
        if(result["method"]=="Update"):
            item_db:models.Item = db.query(models.Item).filter((models.Item.id == result["uuid"])).first()
            print("Update item")
            print(item_db.name)
            try:
               item_db.name = result["name"]
               item_db.amount = result["amount"]
               item_db.description = result["description"]
               item_db.warehouse = result["warehouse_id"]
            except Exception as error:
                print(f"### Update could not be preformed: {type(error).__name__} ---- {error}")
            print(item_db.name)
            
            db.commit()
            return item_db        
        if(result["method"]=="Delete"):
            warehouse_db:models.Warehouse = db.query(models.Warehouse).filter((models.Warehouse.id == result["uuid"])).first()
            print("Detele warehouse")
            print(warehouse_db.address)
            try:
                db.delete(warehouse_db)
            except Exception as error:
                print(f"### Delete could not be preformed: {type(error).__name__} ---- {error}")
            
            db.commit()
            return warehouse_db        

    
    
channel.basic_consume(queue="wab_project",
                      auto_ack=True,
                      on_message_callback=on_message_callback)
channel.start_consuming()
