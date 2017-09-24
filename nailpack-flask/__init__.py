from flask import Flask
from nails import Nailpack
import routes

# app = Flask(__name__)

# @app.route('/')
# def hello_world():
#         return 'Hello, World!'

class Nailpack(Nailpack):
    def __init__(self):
        print('constructing')

    def validate(self, payload):
        print('validating')

    def configure(self, payload):
        self.server = Flask(__name__)
        # routes.register(self.server, self.api.config.routes)

    def initialize(self, payload):
        print('initializing')
