from argparse import RawTextHelpFormatter, ArgumentParser
import copy
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
from gendiff.formatters import format_stylish, format_plain, format_to_json

FORMATTERS = {
    'stylish': format_stylish,
    'plain': format_plain,
    'json': format_to_json
}

LOADERS = {
    'json': json.load,
    'yml': lambda f: YAMLload(f, YAMLLoader),
    'yaml': lambda f: YAMLload(f, YAMLLoader)
}


def sort_nodes(tree):
    if is_list(tree):
        tree.sort(key=sort_nodes)
        return inf
    if is_dict(tree):
        return sort_dict(tree)


def sort_dict(tree):
    values = tree.get('values')
    children = tree.get('children')
    value = values if values is not None else children
    if is_list(value):
        value.sort(key=sort_nodes)
    key = tree.get('key')
    return key if key is not None else inf


def sorted_tree(tree):
    tree_copy = copy.deepcopy(tree)
    tree_copy.sort(key=sort_nodes)
    return tree_copy


def generate_node(key, node_type, values, status):
    return {'key': key, node_type: values, 'status': status}


def get_node_type(node1, node2):
    return 'children' if is_dict(node1) or is_dict(node2) else 'values'


def get_status_of_changed_node(node1, node2):
    return STATUSES['same'] if is_dict(node1) and is_dict(node2) \
        else STATUSES['changed']


def compare_nodes(node1, node2):
    node_type = get_node_type(node1, node2)
    if node1 == node2:
        values = node1
        status = STATUSES['same']
    elif node1 is not Nothing and node2 is not Nothing:
        values = {'old': node1, 'new': node2}
        status = get_status_of_changed_node(node1, node2)
    elif node1 is Nothing and node2 is not Nothing:
        values = node2
        status = STATUSES['added']
    else:
        values = node1
        status = STATUSES['removed']
    return node_type, values, status


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
    if is_dict(node):
        node = [node]
    if is_list(new_node):
        node.extend(new_node)
    else:
        node.append(new_node)
    return node


def generate_future_children_status(parent, status, children_status):
    if parent is None:
        return None
    elif status != STATUSES['same']:
        return STATUSES['same']
    else:
        return children_status


def compare(obj1, obj2, parent=None, children_status=None):
    tree = []
    node_type, values, status = compare_nodes(obj1, obj2)
    future_children_status = generate_future_children_status(
        parent,
        status,
        children_status
    )
    current_status = children_status or status

    if node_type == 'values':
        node = generate_node(parent, node_type,
                             values,
                             current_status)
        return add_node_to_tree(tree, node)

    node = compare_nested_objects(obj1, obj2,
                                  children_status=future_children_status)
    new_node = compare_nested_objects(obj2, obj1,
                                      children_status=future_children_status,
                                      get_old=False)
    add_node_to_tree(node, new_node)

    if parent is not None:
        node = generate_node(parent, node_type, node,
                             children_status or current_status)
    return add_node_to_tree(tree, node)


def open_file(filename):
    return open(filename, 'r', encoding='utf-8')


def converse_file_to_dict(file, filename):
    ext = filename.split('.')[-1]
    return LOADERS[ext](file)


def generate_diff(first_file, second_file, formatter='stylish'):
    file1 = open_file(first_file)
    file2 = open_file(second_file)
    diff = sorted_tree(compare(converse_file_to_dict(file1, first_file),
                       converse_file_to_dict(file2, second_file)))
    return FORMATTERS[formatter](sorted_tree(diff))


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
