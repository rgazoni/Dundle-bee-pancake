#https://www.rabbitmq.com/tutorials/tutorial-four-python.html
#https://medium.com/@rahulsamant_2674/python-rabbitmq-8c1c3b79ab3d
#https://realpython.com/absolute-vs-relative-python-imports/

#!/usr/bin/env python3
from rabbitmq import rabbit


class Subscriber(rabbit.RabbitSetup):

    def __init__(self, config, on_message_callback_func):
        super().__init__(config)
        self.on_message_callback_func = on_message_callback_func

    def __del__(self):
        self.connection.close()

    def _on_message_callback(self, channel, method, properties, body):
        binding_key = method.routing_key
        print("\n")
        print("received new message for -" + binding_key)
        print("\n")
        print(" [x] Received %r" % body)
        print("\n")
        print(" [x] Received %r" % properties)
        print("\n")
        print(" [x] Received %r" % channel)

        #try:
        #    self.on_message_callback_func()
        #except Exception as e:
        #    print(e)

    def consume_from_queue(self, queueName):

        #se nao tiver a queue?

        self.channel.basic_consume(queue=queueName,
            on_message_callback=self._on_message_callback, auto_ack=True)
        print("I'm going to start consuming")
        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.channel.stop_consuming()