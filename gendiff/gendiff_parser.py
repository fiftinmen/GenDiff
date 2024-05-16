from argparse import RawTextHelpFormatter, ArgumentParser
from gendiff.diff_tools import build_diff
from gendiff.formatters import (
    json_formatter,
    plain_formatter,
    stylish_formatter
)
from gendiff.loaders import load

FORMATTERS = {
    'stylish': stylish_formatter.format_diff,
    'plain': plain_formatter.format_diff,
    'json': json_formatter.format_diff
}


def generate_diff(file1, file2, formatter='stylish'):
    diff = build_diff(load(file1),
                      load(file2))
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
