from importlib import import_module
from nails import config
from peewee import *
import datetime
import os
import pydash as _
import re

db = None

if config['database']['driver'] == 'postgres':
    db = PostgresqlDatabase(
        'postgres',
        user=config['database']['user'],
        password=config['database']['password'],
        host=config['database']['host'],
        port=config['database']['port']
    )

def get_models_list(models):
    models_list = list()
    for key in _.keys(models):
        matches = re.findall(r'.+Model$', key)
        if len(matches) > 0:
            models_list.append(getattr(models, matches[0]))
    return models_list

def init_models(file, blueprint, models):
    db.connect()
    models = get_models_list(models)
    db.create_tables(models, safe=True)
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
