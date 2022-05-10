#!/usr/bin/env python3
import json
from rabbitmq import Subscriber

config = {
    'host': '172.40.1.13',
    'port': '5672',
    'exchange': 'amq.direct',
}

class Agent(Subscriber.Subscriber):

<<<<<<< HEAD
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
=======
sub = subscriber.Subscriber(config, 'oi')
print("STOCK")
sub.consume_from_queue('stock')

# Module Imports
import mariadb
import sys

# Connect to MariaDB Platform
try:
    connexion = mariadb.connect(
        user="root",
        password="root",
        host="127.0.0.1",
        port=3307,
        database="Storage"

    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Get Cursor
cursor = connexion.cursor()

command = f'SELECT ID_PROD, ID_CATEGORIA, Nome, Quantidade, lote, origem, Data_fabricacao, Data_vencimento  ' \
          f'FROM produto ' \
          f'INNER JOIN categorias ' \
          f'ON fk_Categorias_ID_CATEGORIA = ID_CATEGORIA'
cursor.execute(command)
query_result = cursor.fetchall() # Retorna a lista de produtos geral
print(query_result)

# Aqui você passa os argumentos para a procedure a ordem seria
# ID_PROD, ID_CATEGORIA, Quantidade, Data_fabricacao,
# Data_vencimento, lote, origem , result -> Deixar 0 por padrão
args = [1, 1, 1, "2001-01-22", "2010-10-23", 17, "Nestlé Campinas", 0]
result_args = cursor.callproc('recebe_produto', args)
result = cursor.fetchall()

print(result[0][0])

cursor.close()
cursor = connexion.cursor()

connexion.commit()


cursor.close()
connexion.close()
>>>>>>> c7b2198 (changed agents)
