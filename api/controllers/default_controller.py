from flask_restful import Resource

class Root(Resource):
    def get(self):
        return 'I am the root'

class Info(Resource):
    def get(self):
        return 'I am info'
