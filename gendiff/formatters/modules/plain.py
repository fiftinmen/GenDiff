from gendiff.structured_dicts import (
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
        stringified_value: f"'{stringified_value}'",
        'True': 'true',
        'False': 'false',
        'None': 'null',
    }.get(str(value), str(value))


def generate_view(node, key, status, values):
    old_value = format(values)
    new_value = None
    if status == STATUSES['changed']:
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
