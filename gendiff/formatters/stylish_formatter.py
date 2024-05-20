from gendiff.diff_tools import (
    get_key,
    get_status,
    get_value,
)

SIGNS = {
    'added': '+',
    'removed': '-',
    'nested': ' ',
    'unchanged': ' ',
    'complex_end': ' '
}

DEFAULT_LEVEL = 1
FILLER = '  '

DICTIONARY_START = '{\n'
DICTIONARY_END = '}\n'


def format_value(value):
    stringified_value = str(value)
    return {
        bool: stringified_value.lower(),
        type(None): 'null',
    }.get(type(value), stringified_value)


def generate_view(level, status, key='', value='', *, separator=': '):
    if isinstance(value, dict):
        return handle_complex_value(level, status, key, value)
    else:
        return [f'{FILLER * level}{SIGNS[status]} {key}{separator}',
                f'{format_value(value)}\n']


def handle_complex_value(level, status, key, value):
    start = generate_view(level, status, key, separator=': {')
    end = generate_view(level, 'complex_end', separator='}')
    views = []
    for key, value in value.items():
        if isinstance(value, dict):
            value = dict(sorted(value.items()))
            views.extend(handle_complex_value(
                level + 2,
                'unchanged',
                key,
                value
            ))
        else:
            views.extend(generate_view(level + 2, 'unchanged', key, value))
    return start + views + end


def handle_updated_value(level, key, value):
    old_value, new_value = value
    return generate_view(level, 'removed', key, old_value) + \
        generate_view(level, 'added', key, new_value)


def handle_node(node, level=DEFAULT_LEVEL):
    status = get_status(node)
    key = get_key(node)
    value = get_value(node)

    if status == 'updated':
        return handle_updated_value(level, key, value)
    elif status == 'nested':
        start = generate_view(level, status, key, separator=': {')
        end = generate_view(level, status, separator='}')
        return start + handle_diff(value, level + 2) + end
    else:
        return generate_view(level, status, key, value)


def handle_diff(diff, level=DEFAULT_LEVEL):
    views = []
    for node in diff:
        views.extend(handle_node(node, level))
    return views


def format_diff(diff):
    result = ''.join(handle_diff(diff)).rstrip()
    return f'{DICTIONARY_START}{result}\n{DICTIONARY_END}'.strip()
