from importlib import import_module
from nails import config
from peewee import *
import datetime
import os
import pydash as _
import re

db = None

if config.database['driver'] == 'postgres':
    db = PostgresqlDatabase(
        'postgres',
        user=config.database['user'],
        password=config.database['password'],
        host=config.database['host'],
        port=config.database['port']
    )

def get_models(path):
    models = list()
    for i in os.listdir(path):
        matches = re.findall(r'.+_model(?=.py$)', i)
        if len(matches) > 0:
            model_package = import_module('api.models.' + matches[0])
            model_name = _.upper_first(_.camel_case(matches[0]))
            models.append(getattr(model_package, model_name))
    return models

def init(file, blueprint):
    db.connect()
    db.create_tables(get_models(os.path.realpath(os.path.dirname(file) + '/models')), safe=True)
    db.close()
    @blueprint.before_request
    def db_connect():
        db.connect()
    @blueprint.teardown_request
    def db_close(exc):
        if not db.is_closed():
            db.close()

class BaseModel(Model):
    created_at = DateTimeField(default=datetime.datetime.now)
    class Meta:
        database = db
