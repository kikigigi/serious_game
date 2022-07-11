from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate, identity
from dotenv import load_dotenv
import os
from collections.abc import Mapping

app = Flask(__name__)
load_dotenv()
app.secret_key = os.getenv('SECRET_KEY')
api = Api(app)
jwt = JWT(app, authenticate, identity)

items = []

class Items(Resource):

    def get(self):
        return {'items': items}

class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help='This filed can not be blanked.')


    @classmethod
    def find_item(cls, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is not None:
            print(f"get item {item['name']}")
        else:
            print('Item is None')
        return item

    @jwt_required()
    def get(self, name):
        item = Item.find_item(name)
        return {'item': item}, 200 if item else 404

    def post(self, name):
        item = Item.find_item(name)
        data = Item.parser.parse_args()
        if item is None:
            items.append({'name': name, 'price': data['price']})
            return {'message': f"{items[-1]['name']} created", 'item': items[-1]}, 201 # created
        return {'message': f"{name} has existed."}, 400 # bad request

    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': f"{name} deleted"}

    def put(self, name):
        item = Item.find_item(name)
        data = Item.parser.parse_args()
        if item:
            item.update(data)
            return {'message': f"{name} price changed."}
        items.append({'name': name, 'price': data['price']})
        return {'message': f"{name} created!"}, 201



api.add_resource(Item, '/item/<string:name>')
api.add_resource(Items, '/items')


if __name__ == '__main__':
    app.run(port=5000, debug=True)