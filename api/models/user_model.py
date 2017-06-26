from nails.models import BaseModel
from peewee import *

class UserModel(BaseModel):
    title = CharField()
