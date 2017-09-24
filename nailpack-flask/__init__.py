from flask import Flask

# app = Flask(__name__)

# @app.route('/')
# def hello_world():
#         return 'Hello, World!'

class Nailpack():
    def __init__(self):
        print('constructing')

    def validate(self, payload):
        print('validating')

    def configure(self, payload):
        self.app = Flask(__name__)
        print('configuring')

    def initialize(self, payload):
        print('initializing')
