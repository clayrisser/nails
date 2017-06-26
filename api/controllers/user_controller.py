from nails import Controller
from api.models import UserModel

class User(Controller):
    def get(self):
        return 'a user'

class UserList(Controller):
    def get(self):
        return 'a list of users'
