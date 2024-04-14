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
    set_sign,
    set_value,
    nested_dict,
    is_nested_dict,
    yield_nested_dict_items,
    sort_nested_dict,
    SIGNS,
)
from gendiff.formatters import stylish, plain

FORMATTERS = {
    'stylish': stylish,
    'plain': plain
}


def parse_dict_list(nested_dict_, formatter=stylish):
    lines = formatter(nested_dict_)
    return '\n'.join(lines)


def compare_nested_dicts(nested_dict1, nested_dict2):
    for structured_dict2 in yield_nested_dict_items(nested_dict2):
        key2 = get_key(structured_dict2)
        value2 = get_value(structured_dict2)
        if structured_dict1 := find_structured_dict_by_key(key2, nested_dict1):
            value1 = get_value(structured_dict1)
            if value1 == value2:
                set_sign(structured_dict1, sign=SIGNS['same'])
            elif is_nested_dict(value1) and is_nested_dict(value2):
                set_sign(structured_dict1, sign=SIGNS['same'])
                set_value(structured_dict1, compare(value1, value2))
            else:
                set_sign(structured_dict1, SIGNS['old'])
                set_sign(structured_dict2, SIGNS['new'])
                nested_dict1.append(structured_dict2)
        else:
            set_sign(structured_dict2, SIGNS['new'])
            nested_dict1.append(structured_dict2)
    return nested_dict1


def compare(dict1, dict2):
    nested_dict1 = nested_dict(dict1, sign=SIGNS['old'])
    if not dict2 or len(dict2) == 0:
        return nested_dict1
    nested_dict2 = nested_dict(dict2, sign=SIGNS['new'])
    if not dict1 or len(dict1) == 0:
        return nested_dict2
    compare_nested_dicts(nested_dict1, nested_dict2)
    return nested_dict1


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
    sort_nested_dict(result)
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
                        help='set format of output:\nstylish (default)\nplain',
                        default='stylish',
                        choices={'stylish', 'plain'}
                        )
    args = parser.parse_args()
    first_file = args.first_file
    second_file = args.second_file
    formatter = FORMATTERS[args.format]
    diff = generate_diff(first_file, second_file, formatter)
    print(diff)
