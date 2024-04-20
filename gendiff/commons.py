STATUSES = {
    'same': ' ',
    'old': '-',
    'new': '+',
    'added': '+',
    'removed': '-',
    'changed': '-+'
}
DEFAULT_STATUS = STATUSES['same']
DEFAULT_LEVEL = 1
FILLER_TEMPLATE = '  '


def Nothing():
    return


def is_dict(value):
    return isinstance(value, dict)


def is_list(object):
    return isinstance(object, list)


def get_value_by_key(obj, key):
    if is_dict(obj):
        return obj.get(key) if key in obj.keys() else Nothing
    else:
        return obj


def get_values_type(node):
    return 'values' if 'values' in node.keys() else 'children'
