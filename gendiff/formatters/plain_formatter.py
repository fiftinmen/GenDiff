from gendiff.diff_tools import (
    get_key,
    get_status,
    get_value,
)
MESSAGES = {
    'added': 'added with value: {}',
    'removed': 'removed',
    'updated': "updated. From {} to {}"
}


def format_value(value):
    stringified_value = str(value)
    return {
        dict: '[complex value]',
        str: f"'{stringified_value}'",
        bool: stringified_value.lower(),
        type(None): 'null',
    }.get(type(value), stringified_value)


def generate_view(key, status, value1, value2):
    return [f"Property '{key}' was {MESSAGES[status].format(value1, value2)}"]


def handle_node(node, parent=None):
    status = get_status(node)
    if status == 'unchanged':
        return []

    key = get_key(node)
    full_key = f'{parent}.{key}' if parent else key
    if status == 'nested':
        views = []
        for child in node.get('children'):
            views.extend(handle_node(child, full_key))
        return views

    value = get_value(node)
    if status == 'updated':
        value1, value2 = value
        value1, value2 = format_value(value1), format_value(value2)
    else:
        value1 = format_value(value)
        value2 = None
    return generate_view(full_key, status, value1, value2)


def format_diff(diff):
    views = []
    for node in diff:
        views.extend(handle_node(node))
    return '\n'.join(views)
