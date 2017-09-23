import importlib
from inspect import getargspec
import helpers
from pydash import _

events = {}

def register(nailpack_names):
    if type(nailpack_names) is str:
        nailpack_name = nailpack_names
        nailpack = importlib.import_module(nailpack_name).Nailpack()
        for key in helpers.pubkeys(nailpack):
            regsiter_event(key, getattr(nailpack, key))
        return nailpack
    nailpacks = list()
    for nailpack_name in nailpack_names:
        nailpack = importlib.import_module(nailpack_name).Nailpack()
        for key in helpers.pubkeys(nailpack):
            regsiter_event(key, getattr(nailpack, key))
        nailpacks.append(nailpack)
        return nailpacks

def regsiter_event(event_name, cb):
    if event_name not in events:
        events[event_name] = [cb]
        return events
    events[event_name].append(cb)
    return events

def run_event(event_name, payload=None):
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
