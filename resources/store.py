from db import db
from flask_restful import Resource, reqparse
from models.store_model import StoreModel

class Store(Resource):

    def get(self, name):
        store = StoreModel.find_store_by_name(name)
        if store:
            return store.json()
        return {'message': f"{name} not found."}, 404

    def post(self, name):
        store = StoreModel.find_store_by_name(name)
        if store:
            return {'message': 'A store with that name has already existed!'}, 400

        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            {'message': 'An error occurred saving the store to the database.'}, 500
        return {'message': f"Store {name} created."}, 201

    def delete(self, name):
        store = StoreModel.find_store_by_name(name)
        if store:
            store.delete_from_db()
            return {'message': f"{store['name']} deleted."}
        return {'message': f"{name} not found."}, 404

class Stores(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}
