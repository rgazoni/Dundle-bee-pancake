#!/usr/bin/env python3

from rabbitmq import rabbit

class Publisher(rabbit.RabbitSetup):

    def __init__(self, config):
        super().__init__(config)

    def __del__(self):
        self.connection.close()

    def publish_message(self, routing_key, message):
        
        try:
            #Publishes message to the exchange with the given routing key
            self.channel.basic_publish(exchange=self.config['exchange'],
            routing_key=routing_key, body=message)
            print("[x] Sent message %r for %r" % (message,routing_key))
        except Exception as e:
            print(e)