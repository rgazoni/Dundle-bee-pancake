#!/usr/bin/env python3
import resource
from flask import Flask
from flask_restful import Api, Resource, reqparse
from rabbitmq import publisher
import json

config = {
    'host': '172.40.1.13',
    'port': '5672',
    'exchange': 'main.exch',
}

app = Flask(__name__)
api = Api(app)
publ = publisher.Publisher(config)

# --------- ARGS ---------
# EXAMPLE:
# CREATE "THE PAYLOAD"
    #teste_args = reqparse.RequestParser()
# ADDING DE ARGUMENTS
    #teste_args.add_argument("name", type=str, help="Name of the product", required=True)
    #help = The err msg if the argument is not passed and if the required is true
    #required = It's necessary

# --------- CODES TO RABBITMQ ---------
#1XX = CODES TO INTERNAL STOCK
#2XX = CODES TO SHELVES

insert_int_stk_args = reqparse.RequestParser()
insert_int_stk_args.add_argument("prod_id", type=int, help="Product ID is necessary", required=True)
insert_int_stk_args.add_argument("prod_cat_id", type=int, help="Product category is necessary", required=True)
insert_int_stk_args.add_argument("prod_qnt", type=int, help="Product quantity is necessary", required=True)
insert_int_stk_args.add_argument("prod_fab_date", type=str, help="Product fab date is necessary", required=True)
insert_int_stk_args.add_argument("prod_val_date", type=str, help="Product val date is necessary", required=True)
insert_int_stk_args.add_argument("prod_batch", type=str, help="Product batch date is necessary", required=True)
insert_int_stk_args.add_argument("prod_origin", type=str, help="Product batch date is necessary", required=True)

insert_shelf_args = reqparse.RequestParser()
insert_shelf_args.add_argument("prod_id", type=int, help="Product ID is necessary", required=True)
insert_shelf_args.add_argument("prod_qnt", type=int, help="Product quantity is necessary", required=True)

remove_shelf_args = reqparse.RequestParser()
remove_shelf_args.add_argument("prod_id", type=int, help="Product ID is necessary", required=True)
remove_shelf_args.add_argument("prod_qnt", type=int, help="Product quantity is necessary", required=True)

check_item_args = reqparse.RequestParser()
check_item_args.add_argument("prod_id", type=int, help="Product ID is necessary", required=True)

# ------------------------

#Insert item to the internal stock
class insert_int_stk(Resource):
    def post(self):
        #getting the args
        args = insert_int_stk_args.parse_args()

        #sendind payload to rabbitMQ
        publ.publish_message('stock.r', json.dumps(args))

        return {"Product": args}


#Get all the items from the internal stock
class get_int_stock(Resource):
    def get(self):
        #sendind a request to rabbitMQ
       
        get_info = {
            "request_type": 101
        }

        #sendind payload to rabbitMQ
        publ.publish_message('stock.r', json.dumps(get_info))

        #list = 

        return {"Products": list}


#Take items from the internal stock and send to the shelf
class insert_shelf(Resource):
    def post(self):
        #array of products_id and qnt
        args = insert_shelf_args.parse_args()

        publ.publish_message('stock.shelves.r', json.dumps(args))

        return '', 204

#Remove item from the shelf
class remove_shelf(Resource):
    def delete(self):
        #array of products_id and qnt
        args = insert_int_stk_args.parse_args()

        #sendind payload to rabbitMQ
        publ.publish_message('shelves.r', json.dumps(args))

        return '', 204

#Get the items name
class check_item(Resource):
    def post(self):
        #getting the args
        args = check_item_args.parse_args()

        #add request_type into args JSON

        #sendind payload to rabbitMQ to get the product name
        publ.publish_message('stock.r', json.dumps(args))

        #item_name = 

        #return the item_name
        return #item_name, 204


# --------- ROUTES ---------
api.add_resource(insert_int_stk, "/insert_int_stock")
api.add_resource(get_int_stock, "/int_stock")
api.add_resource(insert_shelf, "/insert_shelf")
api.add_resource(remove_shelf, "/remove_shelf")
api.add_resource(check_item, "/check_item")

# ------------------------


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
