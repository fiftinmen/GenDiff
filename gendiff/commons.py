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


def get_value(obj, key):
    return obj.get(key, Nothing) if is_dict(obj) else obj


def get_node_type(node):
    return 'values' if 'values' in node.keys() else 'children'
