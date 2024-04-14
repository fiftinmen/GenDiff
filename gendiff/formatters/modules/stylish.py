from gendiff.structured_dicts import (
    get_key,
    get_sign,
    get_value,
    is_nested_dict,
    yield_nested_dict_items,
    FILLER_TEMPLATE,
    DEFAULT_LEVEL,
)


DICTIONARY_START = '{'
DICTIONARY_END = '}'


def format(value):
    return {
        'True': 'true',
        'False': 'false',
        'None': 'null'
    }.get(str(value), str(value))


def generate_view(object, filler=FILLER_TEMPLATE, level=DEFAULT_LEVEL):
    view = ''
    sign = get_sign(object)
    key = get_key(object)
    value = get_value(object)
    if not is_nested_dict(value):
        formatted_value = format(value)
        view = (f'{filler * level}{sign} {key}: '
                f'{formatted_value}')
    else:
        nested_view = '\n'.join([generate_view(atom, filler, level + 2)
                                for atom in yield_nested_dict_items(value)])
        view = (f'{filler * level}{sign} {key}: {DICTIONARY_START}\n'
                f'{nested_view}\n'
                f'{filler * (level+1)}{DICTIONARY_END}')
    return view


def stylish(nested_dict, filler=FILLER_TEMPLATE):
    return [DICTIONARY_START] \
        + [generate_view(atom, filler)
           for atom in yield_nested_dict_items(nested_dict)] \
        + [DICTIONARY_END]
