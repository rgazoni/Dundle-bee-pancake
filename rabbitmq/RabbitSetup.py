#!/usr/bin/env python3
import pika

class RabbitSetup:

    def __init__(self, config):
        self.config = config
        self.connection = self._create_connection()
        self.channel = self.connection.channel()
        self.queuesAndRoutingKeys = {
            'stock' : ['stock'],
            'stock.shelves' : ['stock.shelves'],
            'shelves': ['shelves'],
            'logstash': ['shelves', 'stock.shelves', 'stock']
        }
        self._setup()

    def _create_connection(self):
        parameters=pika.ConnectionParameters(host=self.config['host'],
                                             port=self.config['port'])
        return pika.BlockingConnection(parameters)

    def _setup(self):
    
        #Declaring an exchange routing agent
        self.channel.exchange_declare(exchange=self.config['exchange'],
                                 exchange_type='direct')

        # This method creates or checks a queue. 
        # Good programming practise.
        # durable for message persistence
        for queue in self.queuesAndRoutingKeys:

            result = self.channel.queue_declare(queue=queue, durable=True)
            queue_name = result.method.queue

            for routing_key in self.queuesAndRoutingKeys[queue]:
                #Basic
                self.channel.queue_bind(exchange=self.config['exchange'],
                           queue=queue_name,
                           routing_key=routing_key)

        self.channel.basic_qos(prefetch_count=1)
