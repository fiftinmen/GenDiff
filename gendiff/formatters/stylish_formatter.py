import pprint
SIGNS = {
    'added': '+',
    'removed': '-',
    'updated': '-+',
    'nested': ' ',
    'unchanged': ' '
}

DEFAULT_LEVEL = 1
FILLER = '  '

DICTIONARY_START = '{'
DICTIONARY_END = '}'


def format_value(value):
    return {
        'True': 'true',
        'False': 'false',
        'None': 'null'
    }.get(str(value), str(value))


def generate_line(level, status, key, value):
    return (f'{FILLER * level}{SIGNS[status]} {key}: {value}')


def generate_nested_view(tree, key, status, level):
    nested_view = "\n".join(
        view for node in tree
        if (view := generate_view(node, level + 2))
    )
    start = end = ''
    if (key and status) is not None:
        start = f'{FILLER * level}{SIGNS[status]} {key}: {DICTIONARY_START}\n'
        end = f'{FILLER * (level + 1)}{DICTIONARY_END}'
    return f'{start}{nested_view}\n{end}'


def handle_changes(node, key, level):
    old_value = node.get('old')
    new_value = node.get('new')
    statuses = ('removed', 'added')
    node = [old_value, new_value]
    view = []
    for status, current_value in zip(statuses, (old_value, new_value)):
        if isinstance(current_value, list):
            current_view = generate_nested_view(current_value,
                                                key,
                                                status,
                                                level)
        else:
            current_view = generate_line(level,
                                         status, key,
                                         format_value(current_value))
        view.append(current_view)
    return '\n'.join(view)


def generate_view(node, level=DEFAULT_LEVEL):
    status = node.get('status')
    key = node.get('key')
    values = node.get('children') or node.get('values')

    if status == 'updated':
        return handle_changes(values, key, level)
    elif isinstance(values, list):
        return generate_nested_view(values, key, status, level)
    else:
        return generate_line(level, status, key, format_value(values))


def format_diff(tree):
    return '\n'.join([DICTIONARY_START,
                     *[view for node in tree
                      if (view := generate_view(node)) is not None],
                     DICTIONARY_END])
