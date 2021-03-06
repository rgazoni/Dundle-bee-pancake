#!/usr/bin/env python3
import uuid
from rabbitmq import RabbitSetup
import pika

class Publisher(RabbitSetup.RabbitSetup):

    def __init__(self, config):
        super().__init__(config)

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.queue_bind(exchange=self.config['exchange'],
                           queue=self.callback_queue,
                           routing_key=self.callback_queue)

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

    def __del__(self):
        self.connection.close()

    def publish_message(self, routing_key, message):       
        try:
            #Publishes message to the exchange with the given routing key
            self.channel.basic_publish(exchange=self.config['exchange'],
            routing_key=routing_key, body=message)
        except Exception as e:
            print(e)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def publish_message_response(self, routingKey, message):

        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange=self.config['exchange'],
            routing_key=routingKey,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id, 
            ),
            body=message
        )

        while self.response is None:
            self.connection.process_data_events()
        return self.response