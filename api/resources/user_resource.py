from flask_restful import Resource
from api.models.user_model import UserModel

class User(Resource):
    def get(self):
        return 'a user'

class UserList(Resource):
    def get(self):
        return 'a list of users'
