#!/usr/bin/env python3
import json
from rabbitmq import Subscriber
import mariadb
import sys


config = {
    'host': '172.40.1.13',
    'port': '5672',
    'exchange': 'amq.direct',
}

class Agent(Subscriber.Subscriber):

    def __init__(self, config):
        super().__init__(config)

    def on_request(self, ch, method, props, body):

        # '''
        # Do your code in here
        # '''

        binding_key = method.routing_key
        print("\n")
        print("received new message for -" + binding_key)
        print("\n")
        print(" [x] Received %r" % body)
        print("\n")
        print(" [x] Received %r" % props)
        print("\n")
        print(" [x] Received %r" % ch)

        # If it is a get condition, send back the list of items. 
        # And if it is a insert that initially didn't have to send nothing
        # back, put an ACK down the pipeline 
        # Put your message inside this variable to send to the sender
        # The variable is self.response
        self.response = {'number example of stock': 200,
                         'text': 'text example'}
        # It's interesting to notice that the response is converted to string in order to send
        # into the Rabbit pipeline 
        self.response = json.dumps(self.response)

        return super().on_request(ch, method, props, body)

sub = Agent(config)
sub.consume_from_queue_response('stock')
