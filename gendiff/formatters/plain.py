from gendiff.commons import (
    get_node_type,
    is_list,
    STATUSES
)


MESSAGES = {
    '+': 'added with value: {}',
    '-': 'removed',
    '-+': "updated. From {} to {}"
}


def format_value(value):
    if is_list(value):
        return '[complex value]'
    stringified_value = str(value)
    return {
        str: f"'{stringified_value}'",
        bool: stringified_value.lower(),
        type(None): 'null',
    }.get(type(value), str(value))


def generate_view(key, status, values):
    old_value = format_value(values)
    new_value = None
    if status == STATUSES['changed']:
        old_value = format_value(values.get('old'))
        new_value = format_value(values.get('new'))
        status = STATUSES['old'] + STATUSES['new']
    if status != STATUSES['same']:
        return [f"Property '{key}' was "
                f"{MESSAGES[status].format(old_value, new_value)}"]


def handle_node(node, parent=None):
    key = node.get('key')
    full_key = f'{parent}.{key}' if parent else key
    values = node.get(get_node_type(node))
    status = node.get('status')
    views = []
    if is_list(values) and status == STATUSES['same']:
        for sub_node in values:
            views.extend(handle_node(sub_node, full_key))
    elif view := generate_view(full_key, status, values):
        views.extend(view)
    return views


def format_plain(tree):
    views = []
    for node in tree:
        views.extend(handle_node(node))
    return '\n'.join(views)
