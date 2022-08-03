from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from models.attack_model import AttackModel



###class Items(Resource):
class Attacks(Resource):
    @jwt_required(optional=True)
    def get(self):
        user_id = get_jwt_identity()
        if user_id:
            ###items = [item.json() for item in ItemModel.find_all()]
            attacks = [item.json() for item in AttackModel.find_all()]
            ###return {'items': items}
            return {'attacks': attacks}
        return {'message': 'Please login to get the data.'}


###class Item(Resource):
class Attack(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('state', type=float, required=True, help='Every attack needs a state.')
    parser.add_argument('game_id', type=int, required=True, help='Every attack needs a game id.')

    @jwt_required(optional=True)
    def get(self, name):
        try:
            attack = AttackModel.find_attack(name)
        except:
            return {'message': 'An error occurred while finding the item in the database.'}, 500
        if attack:
            return {'attack': attack.json()}
        return {'message': f"{name} not found."}, 404

    @jwt_required(fresh=True)
    def post(self, name):

        try:
            attack = AttackModel.find_attack(name)
        except:
            return {'message': 'An error occurred while finding the attack in the database.'}, 500
        if attack:
            return {'message': f"{name} existed."}, 400 #bad request
        data = Attack.parser.parse_args() #### noted
        attack = AttackModel(name, **data)
        try:
            AttackModel.save_to_db(attack)
        except:
            return {'message': 'An occurred while inserting attack.'}, 500
        return {'message': f'{name} created'}, 201 # created

    @jwt_required(optional=True)
    def delete(self, name):
        # claims = get_jwt() #########################
        # if not claims['is_admin']: #################
        #     return {'message': 'Admin privilege required.'}, 401 ###################

        try:
            attack = AttackModel.find_attack(name)
        except:
            return {'message': 'An error occurred while finding the attack in the database.'}, 500
        if attack:
            attack.delete_from_db()
            return {'message': f'{name} deleted.'}
        return {'message': f'{name} does not exist.'}, 400

    def put(self, name):
        attack = AttackModel.find_attack(name)
        data = Attack.parser.parse_args()
        if attack is None:
            attack = AttackModel(name, **data)
        else:
            attack.price = data['state']

        attack.save_to_db()
        return {'attack': attack.json()}, 201