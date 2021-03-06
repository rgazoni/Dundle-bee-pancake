#https://www.rabbitmq.com/tutorials/tutorial-four-python.html
#https://medium.com/@rahulsamant_2674/python-rabbitmq-8c1c3b79ab3d
#https://realpython.com/absolute-vs-relative-python-imports/

#!/usr/bin/env python3
from rabbitmq import RabbitSetup
import pika

class Subscriber(RabbitSetup.RabbitSetup):

    def __init__(self, config):
        super().__init__(config)

    def __del__(self):
        self.connection.close()

    # If you want to see some feedback about the proccess copy this into the
    # on_request function
    #     binding_key = method.routing_key
    #     print("\n")
    #     print("received new message for -" + binding_key)
    #     print("\n")
    #     print(" [x] Received %r" % body)
    #     print("\n")
    #     print(" [x] Received %r" % properties)
    #     print("\n")
    #     print(" [x] Received %r" % channel)

    def on_request(self, ch, method, props, body):
        '''
        REQUIRED
        Put into the self.response variable your response to the sender.
        After that call return super().on_request(ch, method, props, body)
        to trigger the mechanism
        '''

        print("\n\n\n"+ props.reply_to)

        ch.basic_publish(exchange=self.config['exchange'],
                         routing_key=props.reply_to,
                         properties=pika.BasicProperties(
                             correlation_id=props.correlation_id),
                         body=self.response)
        ch.basic_ack(delivery_tag=method.delivery_tag)


    def consume_from_queue_response(self, qeueName):
        '''
        REQUIRED
        Override function on_request to put an anwser inside the pipeline for the sender
        '''

        self.channel.basic_consume(
            queue=qeueName,
            on_message_callback=self.on_request,
        )
        
        print('Start consuming')
        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.channel.stop_consuming()

