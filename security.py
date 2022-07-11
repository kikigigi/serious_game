from user import User
import hmac


def authenticate(username, password):
    user = User.find_user_by_username(username)
    if user and hmac.compare_digest(user.password, password):
        return user


def identity(payload):
    user_id = payload['identity']
    return User.find_user_by_id(user_id)
