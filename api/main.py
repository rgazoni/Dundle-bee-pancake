#!/usr/bin/env python3
import resource
from flask import Flask
from flask_restful import Api, Resource, reqparse
from rabbitmq import Publisher
from flask_cors import CORS
import json

#Settings to make connection with RabbitMQ
config = {
    'host': '172.40.1.13',
    'port': '5672',
    'exchange': 'amq.direct',
}

app = Flask(__name__)
CORS(app)
api = Api(app)
publ = Publisher.Publisher(config)

# --------- ARGS ---------
# EXAMPLE:
# CREATE "THE PAYLOAD"
    #teste_args = reqparse.RequestParser()
# ADDING DE ARGUMENTS
    #teste_args.add_argument("name", type=str, help="Name of the product", required=True)
    #help = The err msg if the argument is not passed and if the required is true
    #required = It's necessary


insert_int_stk_args = reqparse.RequestParser()
insert_int_stk_args.add_argument("prod_id", type=int, help="Product ID is necessary", required=True)
insert_int_stk_args.add_argument("prod_cat_id", type=int, help="Product category is necessary", required=True)
insert_int_stk_args.add_argument("prod_qnt", type=int, help="Product quantity is necessary", required=True)
insert_int_stk_args.add_argument("prod_fab_date", type=str, help="Product fab date is necessary", required=True)
insert_int_stk_args.add_argument("prod_val_date", type=str, help="Product val date is necessary", required=True)
insert_int_stk_args.add_argument("prod_batch", type=str, help="Product batch date is necessary", required=True)
insert_int_stk_args.add_argument("prod_origin", type=str, help="Product origin is necessary", required=True)

insert_shelf_args = reqparse.RequestParser()
insert_shelf_args.add_argument("items", type=dict, action="append")
# insert_shelf_args.add_argument("prod_id", type=int, help="Product ID is necessary", required=True)
# insert_shelf_args.add_argument("prod_qnt", type=int, help="Product quantity is necessary", required=True)

remove_shelf_args = reqparse.RequestParser()
remove_shelf_args.add_argument("items", type=dict, action="append")
# remove_shelf_args.add_argument("prod_id", type=int, help="Product ID is necessary", required=True)
# remove_shelf_args.add_argument("prod_qnt", type=int, help="Product quantity is necessary", required=True)

get_item_name_args = reqparse.RequestParser()
get_item_name_args.add_argument("prod_id", type=int, help="Product ID is necessary", required=True)

# ------------------------

#Insert item to the internal stock
class insert_int_stk(Resource):
    def post(self):
        #getting the args
        args = insert_int_stk_args.parse_args()

        args = dict(args)

        #Adding the request type to the args
        args['request_type'] = 101

        #Sendind payload to rabbitMQ
        #To stock queue - Recieves an ACK 
        ack = publ.publish_message_response(routingKey='stock',
                                        message=json.dumps(args))

        args = dict(args)
        args['ack'] = str(ack)
        ack = ''
        #To logstash queue
        # publ.publish_message('logstash', json.dumps(args))
        
        return {"response": args}

#Get all the items from the internal stock
class get_int_stock(Resource): 
    def get(self):
        
        #Sendind a request to stock rabbitMQ queue
        get_info = {
            "request_type": 102
        }

        #Sendind payload to rabbitMQ

        #Expecting as a return all items on stock
        fnt_message = publ.publish_message_response(routingKey='stock',
                                        message=json.dumps(get_info))

        #To logstash queue
        #See with Daniel if is interesting ELK recieves the contents on stock
        #Anylise if this message is useful at all
        # publ.publish_message('logstash', json.dumps(get_info)) 

        return {"Products": json.loads(fnt_message)}

#Insert items that were previously on stock and send them to the shelf
class insert_shelf(Resource):
    def post(self):
        #Array of products_id and qnt
        args = insert_shelf_args.parse_args()

        #Validating the payload
        for item in args['items']:
            if(type(item['prod_id']) != int or type(item['prod_qnt']) != int):
                return {"Response": "Error"}

        args['request_type'] = 201

        #Sendind payload to rabbitMQ
        #To stock.shelves queue - Recieves an ACK 
        ack = publ.publish_message_response(routingKey='stock.shelves',
                                        message=json.dumps(args))

        #To logstash queue
        # publ.publish_message('logstash', json.dumps(args))

        return {"Response": args}
        # return 'OK', 200

#Remove item from the shelf
class remove_shelf(Resource):
    def delete(self):
        #Array of products_id and qnt
        args = remove_shelf_args.parse_args()

         #Validating the payload
        for item in args['items']:
            if(type(item['prod_id']) != int or type(item['prod_qnt']) != int):
                return {"Response": "Error"}

        args['request_type'] = 203

        #Sendind payload to rabbitMQ

        #To shelves queue - Recieves an ACK 
        ack = publ.publish_message_response(routingKey='shelves',
                                        message=json.dumps(args))

        #To logstash queue
        # publ.publish_message('logstash', json.dumps(args))

        # return {"Response": args}
        return 'OK', 200

#Get the item name
class get_item_name(Resource):
    def post(self):
        #Getting the args
        get_info = get_item_name_args.parse_args()

        get_info = dict(get_info)

        get_info['request_type'] = 301

        #Sendind payload to rabbitMQ

        #Expecting as a return a certain item from shelves
        item_name = publ.publish_message_response(routingKey='shelves',
                                        message=json.dumps(get_info))

        #To logstash queue
        #See with Daniel if is interesting ELK recieves the contents on stock
        #Anylise if this message is useful at all
        # publ.publish_message('logstash', json.dumps(get_info))

        #Return the item_name
        return json.loads(item_name), 200


#Get the items from shelf
class get_shelf(Resource):
    def get(self):
        #Add request_type into args JSON
        get_info = {
            "request_type": 202
        }
        
        #Sendind payload to rabbitMQ

        #Expecting as a return all items from shelves
        itemsFromShelf = publ.publish_message_response(routingKey='shelves',
                                        message=json.dumps(get_info))

        #To logstash queue
        #See with Daniel if is interesting ELK recieves the contents on stock
        #Anylise if this message is useful at all
        # publ.publish_message('logstash', json.dumps(get_info))

        return {"Products": json.loads(itemsFromShelf)}


# --------- ROUTES ---------
api.add_resource(insert_int_stk, "/insert_int_stock")
api.add_resource(get_int_stock, "/int_stock")
api.add_resource(insert_shelf, "/insert_shelf")
api.add_resource(remove_shelf, "/remove_shelf")
api.add_resource(get_item_name, "/item_name")
api.add_resource(get_shelf, "/shelf")
# ------------------------


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
