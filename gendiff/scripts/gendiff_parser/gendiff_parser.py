from argparse import RawTextHelpFormatter, ArgumentParser
import json
from yaml import load as YAMLload
try:
    from yaml import CLoader as YAMLLoader
except ImportError:
    from yaml import YAMLLoader
from gendiff.structured_dicts import (
    find_structured_dict_by_key,
    get_key,
    get_value,
    set_status,
    set_value,
    is_dict,
    is_tree,
    is_list,
    yield_tree_items,
    sort_tree,
    STATUSES,
)
from gendiff.formatters import stylish, plain, json_formatter

FORMATTERS = {
    'stylish': stylish,
    'plain': plain,
    'json': json_formatter
}


def parse_dict_list(tree_, formatter=stylish):
    lines = formatter(tree_)
    return '\n'.join(lines) if is_list(lines) else lines


def compare_trees(tree1, tree2):
    for structured_dict2 in yield_tree_items(tree2):
        key2 = get_key(structured_dict2)
        value2 = get_value(structured_dict2)
        if structured_dict1 := find_structured_dict_by_key(key2, tree1):
            value1 = get_value(structured_dict1)
            if value1 == value2:
                set_status(structured_dict1, status=STATUSES['same'])
            elif is_tree(value1) and is_tree(value2):
                set_status(structured_dict1, status=STATUSES['same'])
                set_value(structured_dict1, compare(value1, value2))
            else:
                set_status(structured_dict1, STATUSES['old'])
                set_status(structured_dict2, STATUSES['new'])
                tree1.append(structured_dict2)
        else:
            set_status(structured_dict2, STATUSES['new'])
            tree1.append(structured_dict2)
    return tree1


def add_to_tree(tree, key, values_type, values, status):
    tree.append({'key': key, values_type: values, 'status': status})


def compare_values(value1, value2):
    if value1 == value2:
        values = value1
        status = STATUSES['same']
    elif value2 and value1:
        values = {'old': value1, 'new': value2}
        status = STATUSES['changed']
    elif value2:
        values = value2
        status = STATUSES['added']
    else:
        values = value1
        status = STATUSES['removed']
    return values, status


def compare(obj1, obj2, root=None):
    tree = []
    is_dict1 = is_dict(obj1)
    is_dict2 = is_dict(obj2)
    if not (is_dict1 and is_dict2 or root):
        values_type = 'children' if is_dict1 or is_dict2 else 'values'
        values, status = compare_plain(obj1, obj2)
        add_to_tree(tree, root, values_type, values, status)
        return tree

    for key1, value1 in obj1.items():
        value2 = obj2.get(key1) if is_dict2 else obj2
        node = compare(value1, value2, root=key1)
        tree.extend(node)

    if is_dict2:
        for key2, value2 in obj2.items():
            value1 = obj1.get(key2) if is_dict1 else obj1
            node = compare(value1, value2, root=key1)
            tree.extend(node)

    return tree


def generate_diff(first_file, second_file, formatter=stylish):
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
    formatter = FORMATTERS[args.format]
    diff = generate_diff(first_file, second_file, formatter)
    print(diff)
