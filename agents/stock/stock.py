#!/usr/bin/env python3
from rabbitmq import subscriber

config = {
    'host': '172.40.1.13',
    'port': '5672',
    'exchange': 'main.exch',
}


sub = subscriber.Subscriber(config, 'oi')
print("STOCK")
sub.consume_from_queue('stock')