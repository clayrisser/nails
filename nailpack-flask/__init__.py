from flask import Flask, Blueprint
from flask_restful import Api, Resource
from nails import Nailpack, helpers
import routes
import pydash as _

class Nailpack(Nailpack):
    level_override = 'app'

    def __init__(self):
        pass

    def validate(self, payload):
        pass

    def configure(self, payload):
        if self.level == 'app' or self.level == 'api':
            self.server = Flask(__name__)
        if self.level == 'app':
            for api in self.app.get_apis():
                setattr(api, 'server', Blueprint(api.name, __name__))
                resource = Api(api.server)
                for route in api.config.routes:
                    handler = api.get_handler(api, route.handler)
                    resource.add_resource(handler, api.config.main.prefix + route.path)
                self.server.register_blueprint(api.server)

    def initialize(self, payload):
        self.server.run(host=self.app.config.web.host, port=self.app.config.web.port, debug=self.app.config.main.debug)
