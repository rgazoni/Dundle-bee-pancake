#https://www.cloudamqp.com/blog/part4-rabbitmq-for-beginners-exchanges-routing-keys-bindings.html
#https://www.cloudamqp.com/blog/part4-rabbitmq-13-common-errors.html

#!/usr/bin/env python3
import json
from rabbitmq import publisher

config = {
    'host': '172.40.1.13',
    'port': '5672',
    'exchange': 'main.exch',
}

publ = publisher.Publisher(config)

message1 = {
    "message": "Ola mensasagem"
}

message2 ={
    "routing_key": "stock.shelves.r",
    "message": "Ola mensagem"
}

publ.publish_message('stock.r', json.dumps(message1))
publ.publish_message('stock.shelves.r', json.dumps(message2))

