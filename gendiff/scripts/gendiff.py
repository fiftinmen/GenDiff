#!/usr/bin/env python3
import argparse
import json

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


def is_new_key(key1, dict_list):
    for dictionary in dict_list:
        key2 = dictionary.get('key')
        if key1 == key2:
            return False
    return True


def get_item_difference(key, value1, dictionary,
                        filler=FILLER_TEMPLATE):
    result = []
    value2 = dictionary.get(key)
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


def get_key(dictionary):
    return dictionary['key']


def get_value(dictionary):
    return dictionary['value']


def get_sign(dictionary):
    return dictionary['sign']


def get_filler(dictionary):
    return dictionary['filler']


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


def generate_diff(first_file, second_file):
    result = []
    file1 = open(first_file, 'r', encoding='utf-8')
    file2 = open(second_file, 'r', encoding='utf-8')
    json1 = json.load(file1)
    json2 = json.load(file2)

    for key, value in json1.items():
        diff = get_item_difference(key, value,
                                   json2, filler=FILLER_TEMPLATE)
        if diff != []:
            result.extend(diff)

    for key, value in json2.items():
        if is_new_key(key, result):
            new_item = generate_dictionary(key, value,
                                           sign=SIGNS['new'],
                                           filler=FILLER_TEMPLATE)
            result.append(new_item)

    result = sorted(result, key=get_key)
    result = parse_dict_list(result)
    return '{\n' + result + '\n}'


def parse():
    parser = argparse.ArgumentParser(
        prog='gendiff',
        description='Compares two configuration files and shows a difference.'
    )
    parser.add_argument('first_file')
    parser.add_argument('second_file')
    parser.add_argument('-f', '--format', help='set format of output')
    args = parser.parse_args()
    diff = generate_diff(args.first_file, args.second_file)
    print(diff)
    return diff


def main():
    parse()
    return


if __name__ == '__main__':
    main()
