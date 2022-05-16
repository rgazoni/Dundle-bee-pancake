#!/usr/bin/env python3
from rabbitmq import Subscriber
from datetime import date
import mariadb
import json
import sys

config = {
    'host': '172.40.1.13',
    'port': '5672',
    'exchange': 'amq.direct',
}

def connect():
    try:
        connexion = mariadb.connect(
            user="root",
            password="root",
            host="172.40.1.15",
            port=3306,
            database="Storage"
        )
        return connexion
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

def query_stock(connexion):
    names = ['ID_PROD', 'ID_CATEGORIA', 'Nome', 'produto.Quantidade', 'estoque.quantidade',
             'lote', 'origem', 'Data_fabricacao', 'Data_vencimento']
    cursor = connexion.cursor()
    command = f'SELECT ID_PROD, ID_CATEGORIA, Nome, produto.Quantidade, estoque.quantidade, lote, origem, ' \
              f'Data_fabricacao, Data_vencimento  FROM estoque INNER JOIN produto ' \
              f'ON fk_Produto_ID_PROD = ID_PROD INNER JOIN categorias ' \
              f'ON fk_Categorias_ID_CATEGORIA = ID_CATEGORIA;'
    cursor.execute(command)
    query_result = cursor.fetchall()  # Retorna a lista de produtos nas gondulas
    list = []
    for i in range(len(query_result)):
        dict = {}
        for j in range((len(query_result[i]))):
            if isinstance(query_result[i][j], date):
                date_time = query_result[i][j].strftime("%Y-%m-%d")
                dict[names[j]] = date_time
            else:
                dict[names[j]] = query_result[i][j]
        list.append(dict)

    # convert into json
    json_query = json.dumps(list, indent=2)
    cursor.close()
    connexion.close()
    return json_query

def sell_from_shelves(connexion, id_prod, quant):
    cursor = connexion.cursor()
    args = [id_prod, quant, 0]
    cursor.callproc('saida_caixa', args)
    result = cursor.fetchall()
    cursor.close()
    cursor = connexion.cursor()
    connexion.commit()
    cursor.close()
    connexion.close()
    dict = {}
    dict["result"] = result[0][0]
    return json.dumps(dict, indent=2)

def query_item_name(connexion, id):
    names = ['prod_name']
    cursor = connexion.cursor()
    command = f'SELECT Nome FROM gondula INNER JOIN produto ' \
              f'ON fk_Produto_ID_PROD = ID_PROD INNER JOIN categorias ' \
              f'ON fk_Categorias_ID_CATEGORIA = ID_CATEGORIA ' \
              f'WHERE ID_PROD = {id};'
    cursor.execute(command)
    query_result = cursor.fetchall()  # Retorna a lista de produtos nas gondulas
    list = []
    for i in range(len(query_result)):
        dict = {}
        for j in range((len(query_result[i]))):
            if isinstance(query_result[i][j], date):
                date_time = query_result[i][j].strftime("%Y-%m-%d")
                dict[names[j]] = date_time
            else:
                dict[names[j]] = query_result[i][j]
        list.append(dict)

    # convert into json
    json_query = json.dumps(list, indent=2)

    cursor.close()
    connexion.close()
    return json_query

class Agent(Subscriber.Subscriber):

    def on_request(self, ch, method, props, body):
        json_object = json.loads(body)
        print(body)
        if json_object['request_type'] == 301: 
            con = connect()
            result = query_item_name(con, json_object['prod_id'])
            self.response = result
        elif json_object['request_type'] ==202: 
            con = connect()
            result = query_stock(con)
            self.response = result
        elif json_object['request_type'] ==203: 
            for item in json_object['items']:
                con = connect()
                result = sell_from_shelves(con, item['prod_id'],  item['prod_qnt'])
                self.response = result
        else:
            self.response = json.dumps({'Error': "Invalid request"})
        return super().on_request(ch, method, props, body)


sub = Agent(config)

sub.consume_from_queue_response('shelves')
