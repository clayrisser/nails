import nailpacks
import pydash as _
from helpers import pubkeys

class Nails():
    def __init__(self, app):
        self.app = app

    def start(self):
        for api in self.get_apis():
            for route in api.config.routes:
                nailpacks.register(api.config.main.nailpacks)
        nailpacks.run_event('validate')
        nailpacks.run_event('configure')
        nailpacks.run_event('initialize')
        nailpacks.run_event('update')

    def get_apis(self):
        apis = list()
        for key in pubkeys(self.app):
            apis.append(getattr(self.app, key))
        return apis
