def Nothing():
    return


def get_value(obj, key):
    return obj.get(key, Nothing) if isinstance(obj, dict) else obj
