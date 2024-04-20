from gendiff.commons import (
    is_list,
    FILLER_TEMPLATE,
    DEFAULT_LEVEL,
    STATUSES,
    get_values_type
)


DICTIONARY_START = '{'
DICTIONARY_END = '}'


def format(value):
    return {
        'True': 'true',
        'False': 'false',
        'None': 'null'
    }.get(str(value), str(value))


def generate_line(filler, level, status, key, value):
    return (f'{filler * level}{status} {key}: {value}')


def generate_plain_view(node, key, status, filler, level):
    return generate_line(filler, level, status, key, format(node))


def generate_nested_view(tree, key, status, filler, level):
    nested_view = "\n".join(
        view for node in tree
        if (view := generate_view(node, filler, level + 2))
    )
    start = end = ''
    if (key and status) is not None:
        start = f'{filler * level}{status} {key}: {DICTIONARY_START}\n'
        end = f'{filler * (level+1)}{DICTIONARY_END}'
    return f'{start}{nested_view}\n{end}'


def generate_changed_view(node, key, filler, level):
    if is_list(node):
        node = node[0]
    old_value = node.get('old')
    new_value = node.get('new')
    statuses = ('removed', 'added')
    node = [old_value, new_value]
    view = []
    for status, current_value in zip(statuses, (old_value, new_value)):
        if is_list(current_value):
            current_view = generate_nested_view(current_value,
                                                key,
                                                STATUSES[status],
                                                filler,
                                                level)
        else:
            current_view = generate_line(filler, level,
                                         STATUSES[status], key,
                                         format(current_value))
        view.append(current_view)
    return '\n'.join(view)


def generate_view(node, filler=FILLER_TEMPLATE, level=DEFAULT_LEVEL):
    if is_list(node) and len(node)>0:
        return generate_nested_view(node, None, None, filler, level)
    status = node.get('status')
    key = node.get('key')
    values_type = get_values_type(node)
    values = node.get(values_type)

    if status == STATUSES['changed']:
        return generate_changed_view(values, key, filler, level)
    elif is_list(values):
        return generate_nested_view(values, key, status, filler, level)
    else:
        return generate_plain_view(values, key, status, filler, level)


def stylish(tree, filler=FILLER_TEMPLATE):
    return [DICTIONARY_START,
            *[view for node in tree
              if (view := generate_view(node, filler)) is not None],
            DICTIONARY_END]
