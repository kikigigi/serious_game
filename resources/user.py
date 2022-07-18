from flask_restful import Resource, reqparse
from models.user_model import UserModel
from hmac import compare_digest
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt
from blacklist import BLACKLIST

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username', type=str, required=True, help='Username can not be blank.')
_user_parser.add_argument('password', type=str, required=True, help='Password can not be blank.')


class UserRegister(Resource):


    def post(self):
        data = _user_parser.parse_args()
        user = UserModel.find_user_by_username(data['username'])

        if user:
            return {'message': 'A user with that username has already existed'}, 400  # bad request

        user = UserModel(**data)
        user.save_to_db()
        return {'message': 'User created successfully'}, 201 #created

class UserLogin(Resource):
    @classmethod
    def post(cls):
        # get data from parser
        data = _user_parser.parse_args()
        # get user from database
        user = UserModel.find_user_by_username(data['username'])
        # check for matching password
        if user and compare_digest(user.password, data['password']):
            # create access token
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {'access_token': access_token, 'refresh_token': refresh_token}
        return {'message': 'Incorrect username or password.'}, 401 #unautherorised

class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_user_by_id(user_id)
        if not user:
            return {'message': 'User not found.'}, 404
        return user.json()

    def delete(self, user_id):
        user = UserModel.find_user_by_id(user_id)
        if user is None:
            return {'message': f"User not found."}, 404
        user.delete_from_db()
        return {'message': 'User deleted'}

class UserLogout(Resource):
    @jwt_required()
    def post(self):
        jti = get_jwt()['jti'] # jti is JWT ID, a unique identifier for a JWT
        BLACKLIST.add(jti)
        return {'message': 'Successfully logged out.'}


class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}



