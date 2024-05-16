from gendiff.diff_tools import (
    get_key,
    get_status,
    get_values,
    get_values_types
)
MESSAGES = {
    'added': 'added with value: {}',
    'removed': 'removed',
    'updated': "updated. From {} to {}"
}


def format_value(value):
    stringified_value = str(value)
    return {
        str: value if value == '[complex value]' else f"'{stringified_value}'",
        bool: stringified_value.lower(),
        type(None): 'null',
    }.get(type(value), stringified_value)


def generate_view(key, status, value1, value2):
    return [f"Property '{key}' was {MESSAGES[status].format(value1, value2)}"]


def handle_value(value, value_type):
    return '[complex value]' if value_type == 'complex' else format_value(value)


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

    types = get_values_types(node)
    values = get_values(node)

    if status == 'updated':
        value1, value2 = (handle_value(value, type)
                          for value, type in zip(values, types))
    else:
        value1 = handle_value(values, types)
        value2 = None
    return generate_view(full_key, status, value1, value2)


def format_diff(diff):
    views = []
    for node in diff:
        views.extend(handle_node(node))
    return '\n'.join(views)
