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

    
    
channel.basic_consume(queue="wab_project",
                      auto_ack=True,
                      on_message_callback=on_message_callback)
channel.start_consuming()
