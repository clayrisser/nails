from peewee import *
from api.models import BaseModel

class UserModel(BaseModel):
    title = CharField()
