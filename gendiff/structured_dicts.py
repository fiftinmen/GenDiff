from math import inf
from copy import deepcopy
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


def is_dict(value):
    return isinstance(value, dict)


def get_value_by_key(obj, key):
    if is_dict(obj):
        return obj.get(key) if key in obj.keys() else nothing
    else:
        return obj


def nothing():
    return


def get_values_type(node):
    return 'values' if 'values' in node.keys() else 'children'


def is_list(object):
    return isinstance(object, list)


def sort_tree(tree):
    if is_list(tree):
        tree.sort(key=sort_tree)
        return inf
    if is_dict(tree):
        return sort_node(tree)


def sort_node(tree):
    values = tree.get('values')
    children = tree.get('children')
    value = values if values is not None else children
    if is_list(value):
        value.sort(key=sort_tree)
    key = tree.get('key')
    return key if key is not None else inf
