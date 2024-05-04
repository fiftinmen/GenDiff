from argparse import RawTextHelpFormatter, ArgumentParser
import copy
import json
import os
from yaml import load as YAMLload
try:
    from yaml import CLoader as YAMLLoader
except ImportError:
    from yaml import YAMLLoader
from gendiff.formatters import (
    json_formatter,
    plain_formatter,
    stylish_formatter
)

FORMATTERS = {
    'stylish': stylish_formatter.format_diff,
    'plain': plain_formatter.format_diff,
    'json': json_formatter.format_diff
}

LOADERS = {
    '.json': json.load,
    '.yml': lambda f: YAMLload(f, YAMLLoader),
    '.yaml': lambda f: YAMLload(f, YAMLLoader)
}


def Nothing():
    return


def generate_node(key, node_type, values, status):
    return {'key': key, node_type: values, 'status': status}


def add_node_to_tree(tree, node):
    if isinstance(tree, dict):
        tree = [tree]
    if isinstance(node, list):
        tree.extend(node)
    else:
        tree.append(node)
    return tree


def get_values_key(node1, node2):
    return 'children' if isinstance(node1, dict) or \
        isinstance(node2, dict) else 'values'


def get_status_of_updated_node(node1, node2):
    return 'nested' if isinstance(node1, dict) \
        and isinstance(node2, dict) else 'updated'


def compare_nodes(node1, node2):
    values_key = get_values_key(node1, node2)
    if node1 == node2:
        values = node1
        status = 'unchanged'
    elif node1 is not Nothing and node2 is not Nothing:
        values = {'old': node1, 'new': node2}
        status = get_status_of_updated_node(node1, node2)
    elif node1 is Nothing and node2 is not Nothing:
        values = node2
        status = 'added'
    else:
        values = node1
        status = 'removed'
    return values_key, values, status


def handle_non_dict_comparison(obj1, obj2, get_old):
    if obj1 is Nothing:
        return []
    is_dict1 = isinstance(obj1, dict)
    is_dict2 = isinstance(obj2, dict)
    if not is_dict1 and is_dict2:
        return {
            'old': obj1,
            'new': compare_nested_objects(obj2, obj2, get_old)
        }
    if not is_dict2 and obj2 is not Nothing:
        return {
            'new': obj2,
            'old': compare_nested_objects(obj1, obj1, get_old)
        }
    return None


def get_value(obj, key):
    return obj.get(key, Nothing) if isinstance(obj, dict) else obj


def compare_nested_objects(obj1, obj2, parent_status=None, get_old=True):
    result = handle_non_dict_comparison(obj1, obj2, get_old)
    if result is not None:
        return result
    node = []
    is_dict2 = isinstance(obj2, dict)
    for key1, value1 in obj1.items():
        value2 = obj2.get(key1, Nothing) if is_dict2 else obj2
        if get_old:
            node.extend(compare(value1, value2, parent=key1,
                                parent_status=parent_status))
        elif value2 is Nothing:
            node.extend(compare(value2, value1, parent=key1,
                                parent_status=parent_status))
    return node


def compare(obj1, obj2, parent=None, parent_status=None):
    tree = []
    values_key, values, status = compare_nodes(obj1, obj2)

    if parent is None:
        parent_status = None
    elif parent_status:
        status = 'unchanged'
    elif status in {'updated', 'added', 'removed'}:
        parent_status = status

    if values_key == 'values':
        node = generate_node(parent,
                             values_key,
                             values,
                             status)
        return add_node_to_tree(tree, node)

    node = compare_nested_objects(obj1, obj2, parent_status=parent_status)
    new_node = compare_nested_objects(obj2, obj1, get_old=False,
                                      parent_status=parent_status)
    add_node_to_tree(node, new_node)

    if parent is not None:
        node = generate_node(parent, values_key, node, status)
    return add_node_to_tree(tree, node)


def sort_dict(tree):
    value = tree.get('values') or tree.get('children')
    if isinstance(value, list):
        value.sort(key=sort_dict)
    return tree.get('key')


def sorted_tree(tree):
    tree_copy = copy.deepcopy(tree)
    tree_copy.sort(key=sort_dict)
    return tree_copy


def open_file(filename):
    return open(filename, 'r', encoding='utf-8')


def converse_file_to_dict(filename):
    with open(filename) as file:
        ext = os.path.splitext(filename)[1]
        return LOADERS[ext](file)


def generate_diff(file1, file2, formatter='stylish'):
    diff = sorted_tree(compare(converse_file_to_dict(file1),
                               converse_file_to_dict(file2)))
    return FORMATTERS[formatter](diff)


def parse_args():
    parser = ArgumentParser(
        prog='gendiff',
        description='Compares two configuration files and shows a difference.',
        formatter_class=RawTextHelpFormatter
    )
    parser.add_argument('first_file')
    parser.add_argument('second_file')
    parser.add_argument('-f', '--format',
                        dest='formatter',
                        help='set format of output:\nstylish (default)',
                        default='stylish',
                        choices={'stylish', 'plain', 'json'}
                        )
    return parser.parse_args()


def run_gendiff():
    args = parse_args()
    diff = generate_diff(args.first_file, args.second_file, args.formatter)
    print(diff)
