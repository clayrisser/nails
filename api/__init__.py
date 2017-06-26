import os
from flask import Blueprint, render_template
from api.models import db, init
from flask_restful import Api
from api import resources

init()

blueprint = Blueprint(
    'api',
    __name__,
    template_folder=os.path.dirname(os.path.realpath(__file__)) + '/templates'
)

@blueprint.route('/api/')
def route_index():
    return 'api blueprint'

@blueprint.route('/api/v1/')
def route_v1_index():
    return 'api blueprint version 1'

resource = Api(blueprint)
resource.add_resource(resources.User, '/api/v1/user')
resource.add_resource(resources.UserList, '/api/v1/users')

@blueprint.before_request
def _db_connect():
    db.connect()

@blueprint.teardown_request
def _db_close(exc):
    if not db.is_closed():
        db.close()
