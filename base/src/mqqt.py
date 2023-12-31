import pika
conn_params = pika.ConnectionParameters(host='127.0.0.1')

def publish(msg: str):
    conn = pika.BlockingConnection(conn_params)
    channel = conn.channel()
    channel.basic_publish(
        exchange='',
        routing_key='wab_project',
        body=msg
    )
    conn.close()
