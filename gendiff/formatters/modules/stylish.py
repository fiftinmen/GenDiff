from gendiff.structured_dicts import (
    get_key,
    get_status,
    get_value,
    is_tree,
    yield_tree_items,
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
    status = get_status(object)
    key = get_key(object)
    value = get_value(object)
    if not is_tree(value):
        formatted_value = format(value)
        view = (f'{filler * level}{status} {key}: '
                f'{formatted_value}')
        return view
    else:
        nested_view = '\n'.join([generate_view(atom, filler, level + 2)
                                for atom in yield_tree_items(value)])
        view = (f'{filler * level}{status} {key}: {DICTIONARY_START}\n'
                f'{nested_view}\n'
                f'{filler * (level+1)}{DICTIONARY_END}')
        return view


def stylish(tree, filler=FILLER_TEMPLATE):
    return [DICTIONARY_START] \
        + [generate_view(atom, filler)
           for atom in yield_tree_items(tree)] \
        + [DICTIONARY_END]
