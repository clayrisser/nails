from flask import Flask, Blueprint
from flask_restful import Api, Resource
from nails import Nailpack, helpers
import routes
import pydash as _

# app = Flask(__name__)

# @app.route('/')
# def hello_world():
#         return 'Hello, World!'

class Foo(Resource):
    def get(self):
        return 'hi'

class Nailpack(Nailpack):
    def __init__(self):
        print('constructing')

    def validate(self, payload):
        self.level = self._get_level()

    def configure(self, payload):
        if self.level == 'app' or self.level == 'api':
            self.server = Flask(__name__)
        if self.level == 'app':
            for api in self.app.get_apis():
                setattr(api, 'server', Blueprint(api.name, __name__))
                resource = Api(api.server)
                resource.add_resource(Foo, '/foo')
                self.server.register_blueprint(api.server)

    def initialize(self, payload):
        self.server.run(host='0.0.0.0', port=8080, debug=True)

    def _get_level(self):
        if not hasattr(self, 'api'):
            if _.includes(self.app.config.main.nailpacks, 'nailpack-flask'):
                return 'app'
        elif not _.includes(self.app.config.main.nailpacks, 'nailpack-flask'):
                return 'api'
        return 'invalid'
