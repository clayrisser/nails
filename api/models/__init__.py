from peewee import *
from importlib import import_module
import pydash as _
import datetime
import os
import re

db = PostgresqlDatabase(
    'postgres',
    user='postgres',
    password='',
    host='0.0.0.0',
    port='5432'
)

def get_models():
    models = list()
    for i in os.listdir(os.path.dirname(os.path.realpath(__file__))):
        matches = re.findall(r'.+_model(?=.py)', i)
        if len(matches) > 0:
            model_package = import_module('api.models.' + matches[0])
            model_name = _.upper_first(_.camel_case(matches[0]))
            models.append(getattr(model_package, model_name))
    return models

def initialize():
    db.connect()
    for model in get_models():
        model.create_table(True)
    db.close()

class BaseModel(Model):
    created_at = DateTimeField(default=datetime.datetime.now)
    class Meta:
        database = db
