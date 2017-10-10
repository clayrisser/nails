import nailpack
import pydash as _
from app import App

class Nails():
    def __init__(self, app):
        self.app = App(app)

    def start(self):
        nailpack.register(app=self.app)
        apis = self.app.get_apis()
        for api in apis:
            nailpack.register(app=self.app, api=api)
        nailpack.run_event('validate', apis=apis, app=self.app)
        nailpack.run_event('configure', apis=apis, app=self.app)
        nailpack.run_event('initialize', apis=apis, app=self.app)
        nailpack.run_event('update', apis=apis, app=self.app)
