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
    dict = {}
    dict["result"] = result[0][0]
    return json.dumps(dict, indent=2)

class Agent(Subscriber.Subscriber):

    def on_request(self, ch, method, props, body):
        json_objects = json.loads(body)
        print(body)
        if json_objects['request_type'] == 201: 
            for json_object in json_objects['items']:
                con = connect()
                result = move_from_stock_to_shelves(con, json_object['prod_id'],  json_object['prod_qnt'])
                self.response = result
        else:
            result = json.dumps({'Error': "Invalid request"})
            self.response = result
        print(result)
        return super().on_request(ch, method, props, body)


sub = Agent(config)
sub.consume_from_queue_response('stock.shelves')