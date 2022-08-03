from db import db
from flask_restful import Resource, reqparse
from models.game_model import GameModel

class Game(Resource): ### change store to game

    def get(self, name):
        game = GameModel.find_game_by_name(name)
        if game:
            return game.json()
        return {'message': f"{name} not found."}, 404

    def post(self, name):
        game = GameModel.find_game_by_name(name)
        if game:
            return {'message': 'A game with that name has already existed!'}, 400

        game = GameModel(name)
        try:
            game.save_to_db()
        except:
            {'message': 'An error occurred saving the game to the database.'}, 500
        return {'message': f"Game {name} created."}, 201

    def delete(self, name):
        game = GameModel.find_game_by_name(name)
        if game:
            game.delete_from_db()
            return {'message': f"{game['name']} deleted."}
        return {'message': f"{name} not found."}, 404

class Games(Resource):
    def get(self):
        games = GameModel.find_all()
        if games:
            return {'games': [game.json() for game in GameModel.find_all()]}
        return {'message': 'No game found.'}, 404
