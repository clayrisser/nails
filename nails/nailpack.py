import importlib
from inspect import getargspec
import helpers
from pydash import _

def register(app, api=None, nailpack_name=None):
    if api and not hasattr(api, 'get_handler'):
        setattr(api, 'get_handler', get_handler)
    if nailpack_name:
        return register_nailpack(app, api, nailpack_name)
    nailpacks = list()
    if api:
        for nailpack_name in api.config.main.nailpacks:
            nailpack = register_or_get_nailpack(app, api, nailpack_name)
            nailpacks.append(nailpack)
        for nailpack_name in app.config.main.nailpacks:
            nailpack = register_or_get_nailpack(app, None, nailpack_name)
            if hasattr(nailpack, 'level_override') and nailpack.level_override == 'app_as_api':
                nailpack = register_or_get_nailpack(app, api, nailpack_name)
                nailpacks.append(nailpack)
    else:
        for nailpack_name in app.config.main.nailpacks:
            nailpack = register_or_get_nailpack(app, api, nailpack_name)
            nailpacks.append(nailpack)
    return nailpacks

def register_or_get_nailpack(app, api, nailpack_name):
    if api:
        if hasattr(api, '_registered_nailpacks'):
            if _.includes(_.keys(api._registered_nailpacks), nailpack_name):
                return api._registered_nailpacks[nailpack_name]
            nailpack = importlib.import_module(nailpack_name).Nailpack()
            api._registered_nailpacks[nailpack_name] = nailpack
        else:
            nailpack = importlib.import_module(nailpack_name).Nailpack()
            registered_nailpacks = {}
            registered_nailpacks[nailpack_name] = nailpack
            setattr(api, '_registered_nailpacks', registered_nailpacks)
        setattr(nailpack, 'api', api)
    else:
        nailpack = importlib.import_module(nailpack_name).Nailpack()
        if hasattr(app, '_registered_nailpacks'):
            if _.includes(_.keys(app._registered_nailpacks), nailpack_name):
                return app._registered_nailpacks[nailpack_name]
            app._registered_nailpacks.append(nailpack.name)
        else:
            registered_nailpacks = {}
            registered_nailpacks[nailpack_name] = nailpack
            setattr(app, '_registered_nailpacks', registered_nailpacks)
    for key in helpers.pubkeys(nailpack):
        if app:
            regsiter_event(app, key, getattr(nailpack, key))
        if api:
            regsiter_event(api, key, getattr(nailpack, key))
    if app:
        setattr(nailpack, 'app', app)
    setattr(nailpack, 'name', nailpack_name)
    setattr(nailpack, 'level', get_level(nailpack))
    return nailpack

def regsiter_event(app_api, event_name, cb):
    if not hasattr(app_api, '_events'):
        setattr(app_api, '_events', {})
    events = app_api._events
    if event_name not in events:
        events[event_name] = [cb]
        return events
    events[event_name].append(cb)
    return events

def run_event(event_name, app=None, api=None, apis=None, payload=None):
    responses = list()
    if app:
        response = run_single_event(app, event_name, payload)
        responses.append(response)
    if api:
        response = run_single_event(api, event_name, payload)
        responses.append(response)
    if apis:
        for api in apis:
            response = run_single_event(api, event_name, payload)
            responses.append(response)
    if len(responses) == 1:
        return responses[0]
    return responses

def run_single_event(app_api, event_name, payload=None):
    responses = list()
    if not hasattr(app_api, '_events'):
        return responses
    events = app_api._events
    if event_name not in events:
        return
    for cb in events[event_name]:
        if len(getargspec(cb).args) > 1:
            response = cb(payload)
        else:
            response = cb()
        responses.append(response)
    return responses

def get_level(nailpack):
    if hasattr(nailpack, 'level_override'):
        if nailpack.level_override == 'api':
            if hasattr(nailpack, 'api'):
                if _.includes(nailpack.api.config.main.nailpacks, nailpack.name):
                    return 'api'
            elif _.includes(nailpack.app.config.main.nailpacks, nailpack.name):
                return 'app'
        elif nailpack.level_override == 'app_as_api':
            if hasattr(nailpack, 'api'):
                if _.includes(nailpack.api.config.main.nailpacks, nailpack.name):
                    return 'api'
                elif _.includes(nailpack.app.config.main.nailpacks, nailpack.name):
                    nailpack.api.config.main.nailpacks.append(nailpack.name)
                    return 'api'
            elif _.includes(nailpack.app.config.main.nailpacks, nailpack.name):
                return 'app'
    if not hasattr(nailpack, 'api'):
        if _.includes(nailpack.app.config.main.nailpacks, nailpack.name):
            return 'app'
    elif not _.includes(nailpack.app.config.main.nailpacks, nailpack.name):
        if _.includes(nailpack.api.config.main.nailpacks, nailpack.name):
            return 'api'
    return 'invalid'

def get_handler(self, handler):
    controller = getattr(self.controllers, handler[:handler.index('.')])
    return getattr(controller, handler[handler.index('.') + 1:])

class Nailpack():
    def __init__(self, api):
        self.name = None
        self.api = None
        self.app = None
        self.level = None
