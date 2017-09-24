import nailpack
import pydash as _
from helpers import pubkeys

class Nails():
    def __init__(self, app):
        self.app = app

    def start(self):
        for api in self.get_apis():
            for route in api.config.routes:
                nailpack.register(api)
            nailpack.run_event(api, 'validate')
            nailpack.run_event(api, 'configure')
            nailpack.run_event(api, 'initialize')
            nailpack.run_event(api, 'update')

    def get_apis(self):
        apis = list()
        for key in pubkeys(self.app):
            setattr(self.app, 'name', key)
            apis.append(getattr(self.app, key))
        return apis
