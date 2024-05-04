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


def generate_node(key, values_key, values, status):
    return {'key': key, values_key: values, 'status': status}


def combine_old_and_new_values(old, new):
    return {
        'old': old,
        'new': new
    }


def expanded_dict(dictionary):
    result = []
    for key, value in dictionary.items():
        values_key = 'values'
        status = 'unchanged'
        if isinstance(value, dict):
            value = expanded_dict(value)
            values_key = 'children'
            status = 'nested'
        node = generate_node(key, values_key, value, status)
        result.append(node)
    return result


def handle_updated_values(value1, value2):
    is_dict1 = isinstance(value1, dict)
    is_dict2 = isinstance(value2, dict)
    if is_dict1 and is_dict2:
        return 'nested', compare_dicts(value1, value2)
    elif is_dict1:
        return 'updated', combine_old_and_new_values(expanded_dict(value1),
                                                     value2)
    elif is_dict2:
        return 'updated', combine_old_and_new_values(value1,
                                                     expanded_dict(value2))
    else:
        return 'updated', combine_old_and_new_values(value1, value2)


def compare_values(value1, value2):
    is_dict1 = isinstance(value1, dict)
    is_dict2 = isinstance(value2, dict)
    values_key = 'children' if is_dict1 or is_dict2 else 'values'
    if value1 == value2:
        values = value1
        if is_dict1:
            values = expanded_dict(value1)
        status = 'unchanged'
        return values_key, values, status

    status, values = handle_updated_values(value1, value2)
    return values_key, values, status


def get_values_and_status(value):
    if isinstance(value, dict):
        return 'children', expanded_dict(value)
    else:
        return 'values', value


def compare_dicts(dict1, dict2):
    keys1 = set(dict1.keys())
    keys2 = set(dict2.keys())
    keys_union = keys1 | keys2
    diff = []
    for key in keys_union:
        if key in keys1 and key in keys2:
            value1, value2 = dict1[key], dict2[key]
            values_key, values, status = compare_values(value1, value2)
        elif key in keys1:
            values_key, values = get_values_and_status(dict1[key])
            status = 'removed'
        else:
            values_key, values = get_values_and_status(dict2[key])
            status = 'added'

        node = generate_node(key, values_key, values, status)
        diff.append(node)
    return diff


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
    diff = sorted_tree(compare_dicts(converse_file_to_dict(file1),
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
