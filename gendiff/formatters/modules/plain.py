from gendiff.commons import (
    get_values_type,
    is_list,
    STATUSES
)


CHANGES_COMMENTS = {
    '+': 'added with value: {}',
    '-': 'removed',
    '-+': "updated. From {} to {}"
}


def format(value):
    if is_list(value):
        return '[complex value]'
    stringified_value = str(value)
    return {
        str: f"'{stringified_value}'",
        bool: stringified_value.lower(),
        type(None): 'null',
    }.get(type(value), str(value))


def generate_view(node, key, status, values):
    old_value = format(values)
    new_value = None
    if status == STATUSES['changed']:
        if is_list(values):
            values = values[0]
        old_value = format(values.get('old'))
        new_value = format(values.get('new'))
        status = STATUSES['old'] + STATUSES['new']
    if status != STATUSES['same']:
        return [f"Property '{key}' was {CHANGES_COMMENTS[status].format(old_value, new_value)}"]


def handle_node(node, parent=None):
    values_type = get_values_type(node)
    key = node.get('key')
    full_key = f'{parent}.{key}' if parent else key
    values = node.get(values_type)
    status = node.get('status')
    views = []
    if is_list(values) and status == STATUSES['same']:
        for sub_node in values:
            views.extend(handle_node(sub_node, full_key))
    elif view := generate_view(node, full_key, status, values):
        views.extend(view)
    return views


def plain(tree):
    views = []
    for node in tree:
        views.extend(handle_node(node))
    print(views)
    return views
