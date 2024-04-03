#!/usr/bin/env python3
import argparse
import json

SIGNS = {
    'equal': ' ',
    'not equal': '-',
    'new': '+'
}

FILLER_TEMPLATE = '  '


def format(value):
    if isinstance(value, bool):
        return str(value).lower()
    else:
        return str(value)


def generate_line(key, value, sign=SIGNS['equal'], filler=FILLER_TEMPLATE):
    return f'{filler}{format(sign)} {format(key)}: {format(value)}'


def get_item_difference(key, value1, dictionary,
                        filler=FILLER_TEMPLATE, diff=None):
    result = []
    if diff is None:
        value2 = dictionary.get(key)
        if format(value1) == format(value2):
            return [generate_line(key, value1, sign=SIGNS['equal'],
                                  filler=filler)]
        else:
            result = [generate_line(key, value1, sign=SIGNS['not equal'],
                                    filler=filler)]
            if value2 is not None:
                result.append(generate_line(key, value2, sign=SIGNS['new'],
                                            filler=filler))
    else:
        chunk = generate_line(key, value1, sign='', filler='')
        if chunk not in diff:
            result = [generate_line(key, value1, sign=SIGNS['new'],
                                    filler=filler)]
        else:
            result = []
    return result


def get_first_letter(line, filler=FILLER_TEMPLATE):
    line_copy = line
    line_copy = line_copy.replace(filler, '')
    line_copy = line_copy.replace(' ', '')
    line_copy = line_copy.replace('+', '')
    line_copy = line_copy.replace('-', '')
    return line_copy[0]


def generate_diff(first_file, second_file):
    result = []
    file1 = open(first_file, 'r', encoding='utf-8')
    file2 = open(second_file, 'r', encoding='utf-8')
    json1 = json.load(file1)
    json2 = json.load(file2)

    for jso1_key, jso1_value in json1.items():
        diff = get_item_difference(jso1_key, jso1_value,
                                   json2, filler=FILLER_TEMPLATE)
        if diff != []:
            result.extend(diff)

    resulting_str = '\n'.join(result)

    for jso2_key, jso2_value in json2.items():
        diff = get_item_difference(jso2_key, jso2_value, None,
                                   filler=FILLER_TEMPLATE,
                                   diff=resulting_str)
        if diff != []:
            result.extend(diff)

    result = sorted(result, key=get_first_letter)
    resulting_str = '\n'.join(['{', *result, '}'])
    return resulting_str


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
