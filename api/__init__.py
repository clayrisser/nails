from api import controllers
from flask import Blueprint, render_template
from flask_restful import Api
from nails import models, config, register
from pydash import _
import os

blueprint = register(__file__, controllers)

@blueprint.route('/api/')
def route_index():
    print(_.keys(config.routes))
    return 'api blueprint'

@blueprint.route('/api/v1/')
def route_v1_index():
    return 'api blueprint version 1'

# resource = Api(blueprint)
# resource.add_resource(resources.User, '/api/v1/user')
# resource.add_resource(resources.UserList, '/api/v1/users')
