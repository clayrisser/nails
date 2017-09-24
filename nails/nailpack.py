import importlib
from inspect import getargspec
import helpers
from pydash import _

def register(api, nailpack_name=None):
    if nailpack_name:
        nailpack = importlib.import_module(nailpack_name).Nailpack()
        for key in helpers.pubkeys(nailpack):
            regsiter_event(api, key, getattr(nailpack, key))
        return nailpack
    nailpacks = list()
    for nailpack_name in api.config.main.nailpacks:
        nailpack = importlib.import_module(nailpack_name).Nailpack()
        for key in helpers.pubkeys(nailpack):
            regsiter_event(api, key, getattr(nailpack, key))
        nailpacks.append(nailpack)
        return nailpacks

def regsiter_event(api, event_name, cb):
    if not hasattr(api, '_events'):
        setattr(api, '_events', {})
    events = api._events
    if event_name not in events:
        events[event_name] = [cb]
        return events
    events[event_name].append(cb)
    return events

def run_event(api, event_name, payload=None):
    events = api._events
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
