#!/usr/bin/env python3
import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='172.40.1.13'))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)

message = '{"name": "Jane Doe", "date": "20/01/2022", "qtd": "99"}'
channel.basic_publish(
    exchange='',
    routing_key='task_queue',
    body=message,
    properties=pika.BasicProperties(
        delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
    ))
print(" [x] Sent %r" % message)
connection.close()