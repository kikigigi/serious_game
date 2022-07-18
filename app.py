from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager #pip install flask-jwt-extended
from resources.user import UserRegister, User, UserLogin, TokenRefresh, UserLogout
from resources.item import Item, Items
from resources.store import Store, Stores
from dotenv import load_dotenv
import os
from added_utility import get_frist_user ### added
from blacklist import BLACKLIST

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
load_dotenv()
app.secret_key = os.getenv('SECRET_KEY')
api = Api(app)

jwt = JWTManager(app)
@jwt.additional_claims_loader
def add_clams_to_jwt(identity):
    first_user = get_frist_user()

    if first_user:
        if first_user.id == identity:
            return {'is_admin': True}
        return {'is_admin': False}
    return {'message': 'No user in the database.'}, 404
    # if identity == 1:
    #     return {'is_admin': True}
    # return {'is_admin': False}

@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_payload):
    return jwt_payload['jti'] in BLACKLIST


@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({'description': 'Token has expired.',
                    'error': 'token_expired'}), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({'description': 'Signature verification failed.',
                   'error': 'invalid_token'}), 401

@jwt.unauthorized_loader
def missing_token_callback():
    return jsonify({'description': 'Request does not contain an access token.',
                    'error': 'authorisation required'}), 401

@jwt.needs_fresh_token_loader
def token_no_fresh_callback():
    return jsonify({'descriptopn': 'The token is not fresh.',
                    'error': 'fresh_token required'}), 401

@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return jsonify({'description': 'The token has been revoked.',
                    'error': 'token_revoked'}), 401




api.add_resource(Item, '/item/<string:name>')
api.add_resource(Items, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(Stores, '/stores')



if __name__ == '__main__':
    from db import db
    db.init_app(app)

    if app.config['DEBUG']:
        @app.before_first_request
        def create_tables():
            db.create_all()

    app.run(port=5000)