from helpers import pubkeys

class App():
    def __init__(self, app):
        apis = list()
        for key in pubkeys(app):
            if not key == 'config':
                api = getattr(app, key)
                setattr(api, 'name', key)
                apis.append(api)
        self._apis = apis
        self.config = app.config

    def get_apis(self):
        return self._apis
