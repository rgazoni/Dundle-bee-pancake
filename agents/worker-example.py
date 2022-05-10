#!/usr/bin/env python3
from rabbitmq import subscriber

config = {
    'host': '172.40.1.13',
    'port': '5672',
    'exchange': 'main.exch',
}


sub = subscriber.Subscriber(config, 'oi')

sub.consume_from_queue('stock')
sub.consume_from_queue('stock.shelves')
sub.consume_from_queue('shelves')
