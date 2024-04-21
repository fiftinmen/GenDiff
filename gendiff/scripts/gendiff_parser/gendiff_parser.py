from argparse import RawTextHelpFormatter, ArgumentParser
import json
from math import inf
from yaml import load as YAMLload
try:
    from yaml import CLoader as YAMLLoader
except ImportError:
    from yaml import YAMLLoader
from gendiff.commons import (
    is_dict,
    is_list,
    get_value,
    STATUSES,
    Nothing
)
from gendiff.formatters import stylish, plain, json_formatter

FORMATTERS = {
    'stylish': stylish,
    'plain': plain,
    'json': json_formatter
}


def sort_tree(tree):
    if is_list(tree):
        tree.sort(key=sort_tree)
        return inf
    if is_dict(tree):
        return sort_dict(tree)


def sort_dict(tree):
    values = tree.get('values')
    children = tree.get('children')
    value = values if values is not None else children
    if is_list(value):
        value.sort(key=sort_tree)
    key = tree.get('key')
    return key if key is not None else inf


def parse_dict_list(tree, formatter='stylish'):
    lines = FORMATTERS[formatter](tree)
    return '\n'.join(lines) if is_list(lines) else lines


def generate_node(key, values_type, values, status):
    return {'key': key, values_type: values, 'status': status}


def compare_objects(value1, value2):
    is_dict1 = is_dict(value1)
    is_dict2 = is_dict(value2)
    values_type = 'children' if is_dict1 or is_dict2 else 'values'
    if value1 == value2:
        values = value1
        status = STATUSES['same']
    elif value1 is not Nothing and value2 is not Nothing:
        values = {'old': value1, 'new': value2}
        status = STATUSES['same'] if is_dict1 and is_dict2 \
            else STATUSES['changed']
    elif value1 is Nothing and value2 is not Nothing:
        values = value2
        status = STATUSES['added']
    else:
        values = value1
        status = STATUSES['removed']
    return values_type, values, status


def handle_non_dict_comparison(obj1, obj2, get_old, children_status):
    if obj1 is Nothing:
        return []
    if not is_dict(obj1) and obj1 is not Nothing and is_dict(obj2):
        return {
            'old': obj1,
            'new': compare_nested_objects(obj2, obj2, get_old, children_status)
        }
    if not is_dict(obj2) and obj2 is not Nothing:
        return {
            'new': obj2,
            'old': compare_nested_objects(obj1, obj1, get_old, children_status)
        }
    return None


def compare_nested_objects(obj1, obj2, get_old=True,
                           children_status=STATUSES['same']):
    result = handle_non_dict_comparison(obj1, obj2, get_old, children_status)
    if result is not None:
        return result
    node = []
    for key1, value1 in obj1.items():
        value2 = get_value(obj2, key1)
        if get_old:
            node.extend(compare(value1, value2, parent=key1,
                                children_status=children_status))
        elif value2 is Nothing:
            node.extend(compare(value2, value1, parent=key1,
                                children_status=children_status))
    return node


def add_node_to_tree(node, new_node):
    if is_list(node):
        if is_list(new_node):
            node.extend(new_node)
        else:
            node.append(new_node)
        return node


def generate_next_children_status(parent, status, children_status):
    if parent is None:
        return None
    elif status != STATUSES['same']:
        return STATUSES['same']
    else:
        return children_status


def compare(obj1, obj2, parent=None, children_status=None):
    tree = []
    values_type, values, status = compare_objects(obj1, obj2)
    next_children_status = generate_next_children_status(
        parent,
        status,
        children_status
    )
    current_status = children_status or status

    if values_type == 'values':
        node = generate_node(parent, values_type,
                             values,
                             current_status)
        return add_node_to_tree(tree, node)

    node = compare_nested_objects(obj1, obj2,
                                  children_status=next_children_status)
    new_node = compare_nested_objects(obj2, obj1,
                                      children_status=next_children_status,
                                      get_old=False)
    add_node_to_tree(node, new_node)

    if parent is not None:
        node = generate_node(parent, values_type, node,
                             children_status or current_status)
    return add_node_to_tree(tree, node)


def generate_diff(first_file, second_file, formatter='stylish'):
    loaders = {
        'json': json.load,
        'yml': lambda f: YAMLload(f, YAMLLoader),
        'yaml': lambda f: YAMLload(f, YAMLLoader)
    }
    with open(first_file, 'r', encoding='utf-8') as file1, \
            open(second_file, 'r', encoding='utf-8') as file2:
        ext1, ext2 = first_file.split('.')[1], second_file.split('.')[1]
        dict1, dict2 = loaders[ext1](file1), loaders[ext2](file2)
    result = compare(dict1, dict2)
    sort_tree(result)
    return parse_dict_list(result, formatter)


def gendiff_parser():
    parser = ArgumentParser(
        prog='gendiff',
        description='Compares two configuration files and shows a difference.',
        formatter_class=RawTextHelpFormatter
    )
    parser.add_argument('first_file')
    parser.add_argument('second_file')
    parser.add_argument('-f', '--format',
                        dest='format',
                        help='set format of output:\nstylish (default)',
                        default='stylish',
                        choices={'stylish', 'plain', 'json'}
                        )
    args = parser.parse_args()
    first_file = args.first_file
    second_file = args.second_file
    formatter = args.format
    diff = generate_diff(first_file, second_file, formatter)
    print(diff)
