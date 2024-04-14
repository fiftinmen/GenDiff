from gendiff.structured_dicts import (
    get_key,
    get_sign,
    get_value,
    yield_changes_from_nested_dict_items,
    is_list,
    SIGNS
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
    sign = get_sign(object[0])
    value1 = format(get_value(object[0]))
    value2 = None
    if length == 2:
        sign = SIGNS['old'] + SIGNS['new']
        value2 = format(get_value(object[1]))
    if sign != SIGNS['same']:
        return f"Property '{key}' was {CHANGES[sign].format(value1, value2)}"


def plain(nested_dict):
    return [view
            for pair in yield_changes_from_nested_dict_items(nested_dict)
            if (view := generate_view(pair))]
