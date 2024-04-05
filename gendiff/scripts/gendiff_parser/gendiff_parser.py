import argparse
import json
from yaml import load as YAMLload
try:
    from yaml import CLoader as YAMLLoader
except ImportError:
    from yaml import YAMLLoader


SIGNS = {
    'same': ' ',
    'del': '-',
    'new': '+'
}

FILLER_TEMPLATE = '  '


def format(value):
    if isinstance(value, bool):
        return str(value).lower()
    else:
        return str(value)


def generate_line(key, value, sign=SIGNS['same'], filler=FILLER_TEMPLATE):
    return f'{filler}{format(sign)} {format(key)}: {format(value)}'


def generate_dictionary(key, value, sign=SIGNS['same'], filler=FILLER_TEMPLATE):
    return {'key': key, 'value': value, "sign": sign, "filler": filler}


def get_key(dictionary):
    if dictionary:
        key = dictionary.get('key')
        if key:
            return key
        elif len(dictionary) == 1:
            return list(dictionary.keys())[0]


def get_value(dictionary, key=None):
    if dictionary:
        if key is None:
            return dictionary.get('value')
        else:
            return dictionary.get(key)


def get_sign(dictionary, default=SIGNS['same']):
    if dictionary:
        sign = dictionary.get('sign')
        if sign:
            return sign
        return default


def get_filler(dictionary, default=FILLER_TEMPLATE):
    if dictionary:
        filler = dictionary.get('filler')
        if filler:
            return filler
        return default


def is_new_key(key1, dict_list):
    for dictionary in dict_list:
        key2 = get_key(dictionary)
        if key1 == key2:
            return False
    return True


def get_item_difference(key, value1, dictionary,
                        filler=FILLER_TEMPLATE):
    result = []
    value2 = get_value(dictionary, key)
    if format(value1) == format(value2):
        return [generate_dictionary(key, value1,
                                    sign=SIGNS['same'],
                                    filler=filler)]
    else:
        result = [generate_dictionary(key, value1,
                                      sign=SIGNS['del'],
                                      filler=filler)]
        if value2 is not None:
            result.append(generate_dictionary(key, value2,
                                              sign=SIGNS['new'],
                                              filler=filler))
    return result


def parse_dict_list(dict_list):
    lines = []
    for dict in dict_list:
        filler = get_filler(dict)
        sign = get_sign(dict)
        key = get_key(dict)
        value = get_value(dict)
        new_line = generate_line(key=key, value=value, sign=sign, filler=filler)
        lines.append(new_line)
    return '\n'.join(lines)


def get_changes(dict1, dict2, filler=FILLER_TEMPLATE):
    changes = []
    for key, value in dict1.items():
        diff = get_item_difference(key, value,
                                   dict2, filler=filler)
        changes.extend(diff)
    return changes


def add_new_items(target: list[dict], source: dict,
                  filler=FILLER_TEMPLATE) -> list[dict]:
    for key, value in source.items():
        if is_new_key(key, target):
            new_item = generate_dictionary(key, value,
                                           sign=SIGNS['new'],
                                           filler=filler)
            target.append(new_item)


def compare_dicts(dict1, dict2):
    result = []
    if dict1:
        result = get_changes(dict1, dict2, filler=FILLER_TEMPLATE)
    if dict2:
        add_new_items(result, dict2, filler=FILLER_TEMPLATE)
    result = sorted(result, key=get_key)
    result = parse_dict_list(result)
    return '{\n' + result + '\n}'


def generate_diff(first_file, second_file):
    file1 = open(first_file, 'r', encoding='utf-8')
    file2 = open(second_file, 'r', encoding='utf-8')
    if first_file.endswith('.json'):
        dict1 = json.load(file1)
    elif first_file.endswith('.yml') or first_file.endswith('.yaml'):
        dict1 = YAMLload(file1, YAMLLoader)
        print(dict1)

    if second_file.endswith('.json'):
        dict2 = json.load(file2)
    elif second_file.endswith('.yml') or second_file.endswith('.yaml'):
        dict2 = YAMLload(file2, YAMLLoader)
        print(dict2)
    return compare_dicts(dict1, dict2)


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
