#!/usr/bin/env python3
# Module Imports
import mariadb
import sys
from rabbitmq import subscriber

config = {
    'host': '172.40.1.13',
    'port': '5672',
    'exchange': 'main.exch',
}

# sub = subscriber.Subscriber(config, )
# print("stock")
# sub.consume_from_queue('stock')

class Stock(Subscriber):
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
        isOk = add_stock(connexion,  body.ID_PROD, body.ID_CATEGORIA, body.quant, body.fabrication, body.expiration, body.lot, body.origin)
        
if __name__ = "__main__":
    s = Stock(config)
    s.consume_from_queue('stock')

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
    command = f'SELECT ID_PROD, ID_CATEGORIA, Nome, Quantidade, lote, origem, Data_fabricacao, Data_vencimento  ' \
            f'FROM produto ' \
            f'INNER JOIN categorias ' \
            f'ON fk_Categorias_ID_CATEGORIA = ID_CATEGORIA'
    cursor.execute(command)
    query_result = cursor.fetchall()  # Retorna a lista de produtos nas gondulas
    cursor.close()
    connexion.close()
    return query_result

def add_stock(connexion,  ID_PROD, ID_CATEGORIA, quant, fabrication, expiration, lot, origin)
    cursor = connexion.cursor()
    args = [ID_PROD, ID_CATEGORIA, quant, fabrication, expiration, lot, origin, 0]
    cursor.callproc('recebe_produto', args)
    result = cursor.fetchall()
    cursor.close()
    cursor = connexion.cursor()
    connexion.commit()
    cursor.close()
    connexion.close()
    return result[0][0]