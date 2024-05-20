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
    None: '',
}

DEFAULT_LEVEL = 1
FILLER = '  '

DICTIONARY_START = '{\n'
DICTIONARY_END = '}\n'


TYPE_TO_STRING = {
    bool: lambda x: str(x).lower(),
    type(None): lambda _: 'null',
}


def format_value(value):
    return TYPE_TO_STRING.get(type(value), str)(value)


def generate_view(level, status=None, key='', value='', separator=': '):
    if isinstance(value, dict):
        return generate_complex_view(
            level, status, key, dict(sorted(value.items())))
    else:
        return generate_simple_view(
            level, status, key, value, separator=separator
        )


def generate_simple_view(level, status=None, key='', value='', separator=': '):
    return [f'{FILLER * level}{SIGNS[status]} {key}{separator}',
            f'{format_value(value)}\n']


def generate_complex_view(level, status, key, value):
    start = generate_simple_view(level, status, key, separator=': {')
    end = generate_simple_view(level, separator=' }')
    views = []
    for key, value in value.items():
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
        old_value, new_value = value
        return generate_view(level, 'removed', key, old_value) + \
            generate_view(level, 'added', key, new_value)
    elif status == 'nested':
        start = generate_simple_view(level, status, key, separator=': {')
        end = generate_simple_view(level, status, separator='}')
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
