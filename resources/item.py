from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item_model import ItemModel



class Items(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help='Every item needs a name.')
    parser.add_argument('store_id', type=int, required=True, help='Every item needs a store id.')

    @jwt_required()
    def get(self, name):
        try:
            item = ItemModel.find_item(name)
        except:
            return {'message': 'An error occurred while finding the item in the database.'}, 500
        if item:
            return {'item': item.json()}
        return {'message': f"{name} not found."}, 404

    def post(self, name):
        try:
            item = ItemModel.find_item(name)
        except:
            return {'message': 'An error occurred while finding the item in the database.'}, 500
        if item:
            return {'message': f"{name} existed."}, 400 #bad request
        data = Item.parser.parse_args()
        item = ItemModel(name, **data)
        try:
            ItemModel.save_to_db(item)
        except:
            return {'message': 'An occurred while inserting item.'}, 500
        return {'message': f'{name} created'}, 201 # created

    def delete(self, name):
        try:
            item = ItemModel.find_item(name)
        except:
            return {'message': 'An error occurred while finding the item in the database.'}, 500
        if item:
            item.delete_from_db(item)
            return {'message': f'{name} deleted.'}
        return {'message': f'{name} does not exist.'}, 400

    def put(self, name):
        item = ItemModel.find_item(name)
        data = Item.parser.parse_args()
        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']

        item.save_to_db()
        return {'item': item.json()}, 201