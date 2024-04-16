from gendiff.structured_dicts import (
    get_key,
    get_status,
    get_value,
    is_tree,
    is_list,
    yield_tree_items,
    FILLER_TEMPLATE,
    DEFAULT_LEVEL,
    STATUSES,
    is_dict
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


def generate_view(node, filler=FILLER_TEMPLATE, level=DEFAULT_LEVEL):
    view = ''
    status = node.get('status')
    key = node.get('key')
    values = node.get('values')
    children = node.get('children')
    value = values if values is not None else children
    if not is_list(value):
        formatted_value = format(value)
        if status in {STATUSES['same'], STATUSES['removed'], STATUSES['added']}:
            current_view = generate_line(filler, level,
                                         status, key, formatted_value)
            return current_view
        elif status == STATUSES['changed']:
            old_value = value.get('old')
            new_value = value.get('new')
            values = [old_value, new_value]
            view = []
            for i, current_value in enumerate(values):
                if not is_list(current_value):
                    current_view = generate_line(filler, level,
                                                 STATUSES['changed'][i], key,
                                                 format(current_value))
                else:
                    current_view = generate_view(current_value,
                                                 filler,
                                                 level)
                view.append(current_view)
            return '\n'.join(view)
    else:
        nested_view = '\n'.join([generate_view(atom, filler, level + 2)
                                for atom in yield_tree_items(value)])
        view = (f'{filler * level}{status} {key}: {DICTIONARY_START}\n'
                f'{nested_view}\n'
                f'{filler * (level+1)}{DICTIONARY_END}')
        return view


def stylish(tree, filler=FILLER_TEMPLATE):
    print(tree)
    return [DICTIONARY_START] \
        + [generate_view(node, filler)
           for node in yield_tree_items(tree)] \
        + [DICTIONARY_END]
