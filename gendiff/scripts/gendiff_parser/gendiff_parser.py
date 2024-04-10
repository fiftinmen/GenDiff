import argparse
import json
from yaml import load as YAMLload
try:
    from yaml import CLoader as YAMLLoader
except ImportError:
    from yaml import YAMLLoader
from gendiff.atomic_dicts import (
    get_atomic_dict,
    get_key,
    get_sign,
    get_value,
    set_sign,
    set_value,
    nested_dict,
    is_nested_dict,
    get_atoms,
    sort_nested_dict,
    SIGNS,
    FILLER_TEMPLATE,
    DEFAULT_LEVEL,
)


DICTIONARY_START = '{'
DICTIONARY_END = '}'


def format(value):
    if isinstance(value, bool):
        return str(value).lower()
    else:
        return str(value)


def generate_view(object, filler=FILLER_TEMPLATE, level=DEFAULT_LEVEL):
    view = ''
    sign = get_sign(object)
    key = get_key(object)
    value = get_value(object)
    if not is_nested_dict(value):
        if value is None:
            value = 'null'
        view = (f'{filler * level}{format(sign)} {format(key)}: '
                f'{format(value)}')
        return view
    else:
        view = (f'{filler * level}{format(sign)} {format(key)}: '
                f'{DICTIONARY_START}')
        for atom in get_atoms(value):
            sub_view = generate_view(atom, filler, level + 2)
            view = '\n'.join([view, sub_view])
        view_end = (f'{filler * (level+1)}{DICTIONARY_END}')
        view = '\n'.join([view, view_end])
        return view


def parse_dict_list(nested_dict_, filler=FILLER_TEMPLATE, level=DEFAULT_LEVEL):
    lines = [DICTIONARY_START]
    for atom in nested_dict_:
        new_lines = generate_view(atom, filler=filler, level=level)
        lines.append(new_lines)
    lines.append(DICTIONARY_END)
    lines = '\n'.join(lines)
    return lines


def compare_nested_dicts(nested_dict1, nested_dict2):
    for atomic_dict2 in get_atoms(nested_dict2):
        key2 = get_key(atomic_dict2)
        value2 = get_value(atomic_dict2)
        atomic_dict1 = get_atomic_dict(key2, nested_dict1)
        if atomic_dict1:
            value1 = get_value(atomic_dict1)
            if value1 == value2:
                set_sign(atomic_dict1, sign=SIGNS['same'])
            elif is_nested_dict(value1) and is_nested_dict(value2):
                set_sign(atomic_dict1, sign=SIGNS['same'])
                set_value(atomic_dict1, compare(value1, value2))
            else:
                set_sign(atomic_dict1, SIGNS['old'])
                set_sign(atomic_dict2, SIGNS['new'])
                nested_dict1.append(atomic_dict2)
        else:
            set_sign(atomic_dict2, SIGNS['new'])
            nested_dict1.append(atomic_dict2)
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


def generate_diff(first_file, second_file):
    file1 = open(first_file, 'r', encoding='utf-8')
    file2 = open(second_file, 'r', encoding='utf-8')
    if first_file.endswith('.json'):
        dict1 = json.load(file1)
    elif first_file.endswith('.yml') or first_file.endswith('.yaml'):
        dict1 = YAMLload(file1, YAMLLoader)

    if second_file.endswith('.json'):
        dict2 = json.load(file2)
    elif second_file.endswith('.yml') or second_file.endswith('.yaml'):
        dict2 = YAMLload(file2, YAMLLoader)
    result = compare(dict1, dict2)
    sort_nested_dict(result)
    result = parse_dict_list(result)
    return result


def gendiff_parser():
    parser = argparse.ArgumentParser(
        prog='gendiff',
        description='Compares two configuration files and shows a difference.'
    )
    parser.add_argument('first_file')
    parser.add_argument('second_file')
    parser.add_argument('-f', '--format', help='set format of output')
    args = parser.parse_args()
    first_file = args.first_file
    second_file = args.second_file
    diff = generate_diff(first_file, second_file)
    print(diff)
