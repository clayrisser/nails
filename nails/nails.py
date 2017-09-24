import nailpack
import pydash as _
from helpers import pubkeys

class Nails():
    def __init__(self, app):
        self.app = app

    def start(self):
        nailpack.register(app=self.app)
        apis = self.get_apis()
        for api in apis:
            nailpack.register(api=api)
        nailpack.run_event('validate', apis=apis, app=self.app)
        nailpack.run_event('configure', apis=apis, app=self.app)
        nailpack.run_event('initialize', apis=apis, app=self.app)
        nailpack.run_event('update', apis=apis, app=self.app)

    def get_apis(self):
        apis = list()
        for key in pubkeys(self.app):
            if not key == 'config':
                setattr(self.app, 'name', key)
                apis.append(getattr(self.app, key))
        return apis
