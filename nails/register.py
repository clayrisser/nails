import os
import models
import re
from flask import Blueprint, render_template
from flask_restful import Api
from config import config
from pydash import _

def register(file, controllers):
    matches = re.findall(r'(?<=\/).+(?=.__init__.py)', file)
    blueprint = None
    if len(matches) > 0:
        blueprint = Blueprint(
            matches[0],
            __name__,
            template_folder=os.path.dirname(config.base_dir + '/' + matches[0] + '/templates/')
        )
    models.init(file, blueprint)
    resource = Api(blueprint)
    for route, controller_name in config.routes.iteritems():
        controller_name = controller_name.split('.')
        if (len(controller_name) > 1):
            resource.add_resource(getattr(getattr(
                controllers,
                controller_name[0]
            ), controller_name[1]), route)
    return blueprint
