import os
from flask import Flask
from config import config

class Nails(Flask):
    def __init__(self, import_name):
        super(self.__class__, self).__init__(import_name)
        app = self

    def run(self, host=None, port=None, debug=None, **options):
        super(self.__class__, self).run(
            host=host if host else config.nails['host'],
            port=port if port else config.nails['port'],
            debug=debug if debug else config.nails['debug']
        )
