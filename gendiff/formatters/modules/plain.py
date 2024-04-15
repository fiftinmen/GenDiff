from gendiff.structured_dicts import (
    get_key,
    get_status,
    get_value,
    yield_changes_from_tree_items,
    is_list,
    STATUSES
)


CHANGES = {
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


def generate_view(object):
    length = len(object)
    key = get_key(object[0])
    status = get_status(object[0])
    value1 = format(get_value(object[0]))
    value2 = None
    if length == 2:
        status = STATUSES['old'] + STATUSES['new']
        value2 = format(get_value(object[1]))
    if status != STATUSES['same']:
        return f"Property '{key}' was {CHANGES[status].format(value1, value2)}"


def plain(tree):
    return [view
            for pair in yield_changes_from_tree_items(tree)
            if (view := generate_view(pair))]
