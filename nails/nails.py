from config import config, set_app_config
from flask import Flask, Blueprint
from flask_restful import Api
from pydash import _
from models import init_models
import os
import re

class Nails(Flask):
    def __init__(self, import_name):
        super(self.__class__, self).__init__(import_name)
        app = self

    def run(self, host=None, port=None, debug=None, **options):
        super(self.__class__, self).run(
            host=host if host else config['nails']['host'],
            port=port if port else config['nails']['port'],
            debug=debug if debug else config['nails']['debug']
        )

    def register_app(self, app):
        self.register_blueprint(app)

def init_app(filepath, base, controllers, models):
    matches = re.findall(r'[^\/]+(?=.__init__.py)', filepath)
    blueprint = None
    if len(matches) > 0:
        app_name = matches[0]
        set_app_config(app_name)
        blueprint = Blueprint(
            app_name,
            __name__,
            template_folder=os.path.dirname(config['base_dir'] + '/' + app_name + '/templates/')
        )
        init_models(filepath, blueprint, models)
        resource = Api(blueprint)
        for route, controller_name in config['api']['routes'].iteritems():
            controller_name = controller_name.split('.')
            if (len(controller_name) > 1):
                resource.add_resource(getattr(getattr(
                    controllers,
                    controller_name[0]
                ), controller_name[1]), route)
    return blueprint
