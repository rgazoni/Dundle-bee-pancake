#!/usr/bin/env python3
import pika

class RabbitSetup:

    def __init__(self, config):
        self.config = config
        self.connection = self._create_connection()
        self.channel = None
        self.queuesAndRoutingKeys = {
            'stock' : ['stock.r'],
            'stock.shelves' : ['stock.shelves.r'],
            'shelves': ['shelves.r'],
            'logstash': ['shelves.r', 'stock.shelves.r', 'stock.r']
        }
        self._setup()

    def _create_connection(self):
        parameters=pika.ConnectionParameters(host=self.config['host'],
                                             port=self.config['port'])
        return pika.BlockingConnection(parameters)

    def _setup(self):
    
        connection = self.connection

        self.channel = connection.channel()


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
                self.channel.queue_bind(exchange=self.config['exchange'],
                           queue=queue_name,
                           routing_key=routing_key)

        self.channel.basic_qos(prefetch_count=1)
