from flask import Flask, jsonify
from flask_restful import Resource, Api
from dotenv import load_dotenv
import os

load_dotenv()
secret_key = os.getenv('SECRET_KEY')
app = Flask(__name__)
api = Api(app)

class Store(Resource):

    def get(self, name):
        return {'name': name}

class Stores(Resource):

    def get(self):
        stores = []
        return {'stores': stores}

api.add_resource(Store, '/store/<string:name>')
api.add_resource(Stores, '/stores')



if __name__ == '__main__':
    app.run(port=5000, debug=True)