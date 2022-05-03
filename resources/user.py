from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token, create_refresh_token
from models.user import UserModel

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username',
                          type=str,
                          required=True,
                          help="This field is mandatory")

_user_parser.add_argument('password',
                          type=str,
                          required=True,
                          help="This field is mandatory")

class UserRegister(Resource):

    def post(self):
        data = _user_parser.parse_args()
        if UserModel.findByUsername(data['username']) is not None:
            return {"message": "[INFO] An user with username {} already exists.".format(data['username'])}, 400

        user = UserModel(data['username'], data['password'])
        #user = UserModel(**data])
        user.saveToDB()

        return {"message": "[INFO] User with username {} is created successfully.".format(data['username'])}, 201

class User(Resource):
    @classmethod
    def get(cls, userId):
        user = UserModel.findById(userId)
        if not user:
            return {'message': 'No user is found with ID {}'.format(userId)}, 404
        else:
            return user.json()

    @classmethod
    def delete(cls, userId):
        user = UserModel.findById(userId)
        if not user:
            return {'message': 'No user is found with ID {}'.format(userId)}, 404
        else:
            user.deleteFromDB()
            return {'message': 'User with ID {} is deleted'.format(userId)}, 200

class UserLogin(Resource):

    @classmethod
    def post(cls):
        # get data from parser
        data = _user_parser.parse_args()
        # find user in database
        user = UserModel.findByUsername(data['username'])
        if not user:
            return {'message': 'User with username {} does not exist.'.format(data['username'])}
        elif safe_str_cmp(user.password, data['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200
        else:
            return {'message': 'For the Username {}, password entered is incorrect'.format(data['username'])}

