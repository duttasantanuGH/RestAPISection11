from models.user import UserModel

def authenticate(username, password):
    user = UserModel.findByUsername(username)
    if user and password == user.password:
        return user

def identity(payload):
    userid = payload['identity']
    return UserModel.findById(userid)