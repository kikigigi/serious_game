from db import db


class GameModel(db.Model):# change from StoreModel to GameModel
    ###tablename__ = 'stores'
    __tablename__ = 'games'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))


    #items = db.relationship('ItemModel', lazy='dynamic')
    attacks = db.relationship('AttackModel', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def json(self):
        #return {'id': self.id, 'name': self.name, 'items': [item.json() for item in self.items.all()]}
        return {'id': self.id, 'name': self.name, 'attacks': [attack.json() for attack in self.attacks.all()]}

    @classmethod
    def find_game_by_name(cls, name):
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



