from db import db

class AttackModel(db.Model):
    __tablename__ = 'attacks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    state = db.Column(db.Integer)


    game_id = db.Column(db.Integer, db.ForeignKey('games.id'))
    game = db.relationship('GameModel')

    def __init__(self, name, state, game_id):
        self.name = name
        self.state = state
        self.game_id = game_id

    def json(self):
        return {'id': self.id, 'name': self.name, 'state': self.state, 'game_id': self.game_id}

    @classmethod
    def find_attack(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
