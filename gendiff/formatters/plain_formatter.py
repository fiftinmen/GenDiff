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

TYPE_TO_STRING = {
    dict: lambda x: '[complex value]',
    bool: lambda x: str(x).lower(),
    type(None): lambda _: 'null',
    int: lambda x: str(x),
    str: lambda x: f"'{x}'",
}


def format_value(value):
    return TYPE_TO_STRING.get(type(value))(value)


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
        val1, val2 = (format_value(val) for val in value)
    else:
        val1 = format_value(value)
        val2 = None
    return [f"Property '{full_key}' was {MESSAGES[status].format(val1, val2)}"]


def format_diff(diff):
    views = []
    for node in diff:
        views.extend(handle_node(node))
    return '\n'.join(views)
