import importlib
from inspect import getargspec
import helpers
from pydash import _

def register(app, api=None, nailpack_name=None):
    if nailpack_name:
        return register_nailpack(app, api, nailpack_name)
    nailpacks = list()
    app_api = (app if not api else api)
    for nailpack_name in app_api.config.main.nailpacks:
        nailpack = register_nailpack(app, api, nailpack_name)
        nailpacks.append(nailpack)
    return nailpacks

def register_nailpack(app, api, nailpack_name):
    nailpack = importlib.import_module(nailpack_name).Nailpack()
    setattr(nailpack, 'name', nailpack_name)
    if app:
        setattr(nailpack, 'app', app)
    if api:
        setattr(nailpack, 'api', api)
    for key in helpers.pubkeys(nailpack):
        if app:
            regsiter_event(app, key, getattr(nailpack, key))
        if api:
            regsiter_event(api, key, getattr(nailpack, key))
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
    events = app_api._events
    responses = list()
    if event_name not in events:
        return
    for cb in events[event_name]:
        if len(getargspec(cb).args) > 1:
            response = cb(payload)
        else:
            response = cb()
        responses.append(response)
    return responses

class Nailpack():
    def __init__(self, api):
        self.name = None
        self.api = None
        self.app = None
