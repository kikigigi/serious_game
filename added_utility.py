from db import db
from models.user_model import UserModel


def get_frist_user():
    return UserModel.find_first_user()