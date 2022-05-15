#!/usr/bin/env python3
<<<<<<< HEAD
import json
from rabbitmq import Subscriber
=======
# Module Imports
import mariadb
import sys
from rabbitmq import subscriber
>>>>>>> abd69953f1404a9c24e844b28b64bbb6887d8dbe

config = {
    'host': '172.40.1.13',
    'port': '5672',
    'exchange': 'amq.direct',
}

<<<<<<< HEAD
class Agent(Subscriber.Subscriber):

    def on_request(self, ch, method, props, body):

        # '''
        # Do your code in here
        # '''

        # If it is a get condition, send back the list of items. 
        # And if it is a insert that initially didn't have to send nothing
        # back, put an ACK down the pipeline 
        # Put your message inside this variable to send to the sender
        # The variable is self.response
        self.response = {'number example stock shelf': 101,
                         'text': 'text example'}
        # It's interesting to notice that the response is converted to string in order to send
        # into the Rabbit pipeline 
        self.response = json.dumps(self.response)

        return super().on_request(ch, method, props, body)


sub = Agent(config)
sub.consume_from_queue_response('stock.shelves')
=======
# sub = subscriber.Subscriber(config, )
# print("stock.shelves")
# sub.consume_from_queue('stock.shelves')

class StockShelves(Subscriber):
    # def on_message_callback(self, channel, method, properties, body):
    #     binding_key = method.routing_key
    #     print("\n")
    #     print("received new message for -" + binding_key)
    #     print("\n")
    #     print(" [x] Received %r" % body)
    #     print("\n")
    #     print(" [x] Received %r" % properties)
    #     print("\n")
    #     print(" [x] Received %r" % channel)
    #     print("Opa Ramon Bom?")
    def on_message_callback(self, channel, method, properties, body):
        connexion = connect()
        #if query_stock:
        query_result = query_stock(connexion)
        #if sell:
        isOk = move_from_stock_to_shelves(connexion, body.id, body.quantity)
        
if __name__ = "__main__":
    s = StockShelves(config)
    s.consume_from_queue('stock.shelves')

def connect():
    try:
        connexion = mariadb.connect(
            user="root",
            password="root",
            host="127.0.0.1",
            port=3307,
            database="Storage"
        )
        return connexion
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

def query_stock(connexion):
    cursor = connexion.cursor()
    command = f'SELECT ID_PROD, ID_CATEGORIA, Nome, produto.Quantidade, estoque.quantidade, ' \
            f'lote, origem, Data_fabricacao, Data_vencimento FROM estoque INNER JOIN produto ' \
            f'ON fk_Produto_ID_PROD = ID_PROD INNER JOIN categorias ' \
            f'ON fk_Categorias_ID_CATEGORIA = ID_CATEGORIA;'
    cursor.execute(command)
    query_result = cursor.fetchall()  # Retorna a lista de produtos nas gondulas
    cursor.close()
    connexion.close()
    return query_result

def move_from_stock_to_shelves(connexion, ID_PROD, quant):
    cursor = connexion.cursor()
    args = [ID_PROD, quant, 0]
    cursor.callproc('move_gondula', args)
    result = cursor.fetchall()
    cursor.close()
    cursor = connexion.cursor()
    connexion.commit()
    cursor.close()
    connexion.close()
    return result[0][0]
>>>>>>> abd69953f1404a9c24e844b28b64bbb6887d8dbe
