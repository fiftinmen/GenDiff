import json


def format_diff(object):
    result = json.dumps(object)
    print(result)
    return result
