#!/usr/bin/env python3
import json
from rabbitmq import subscriber
from rabbitmq import publisher

config = {
    'host': '172.40.1.13',
    'port': '5672',
    'exchange': 'main.exch',
}

class rabbitApi(subscriber.Subscriber):
    def _on_message_callback(self, channel, method, properties, body):
        return json.loads(body)


sub = rabbitApi(config)
print("STOCK")
l = sub.consume_from_queue('stock')
print(l)


p = publisher.Publisher(config)
p.publish_message('teste.r', json.dumps('ok'))