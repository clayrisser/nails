def pubkeys(obj):
    keys = list()
    for key in (key for key in dir(obj) if not key.startswith('_')):
        keys.append(key)
    return keys
