import pytest
import os
from itertools import product
from gendiff.gendiff_parser import (
    generate_diff,
)
from gendiff.loaders import load, LOADERS

STRUCTURE_TYPES = ['plain', 'nested']
FILE_TYPES = ['json', 'yaml']
TESTS = [['file1', 'file2', 'result_diffs1.txt'],
         ['file1', 'file1', 'result_diffs2.txt'],
         ['file1', 'file3', 'result_diffs3.txt'],
         ['file3', 'file1', 'result_diffs4.txt']]
TEST_FILE1 = 0
TEST_FILE2 = 1
RESULT_FILE = 2
COUNT_OF_TESTS = {'stylish': 4, 'plain': 1, 'json': 1}

TESTS_FOR_STYLISH = list(product(STRUCTURE_TYPES,
                                 FILE_TYPES,
                                 ['stylish'],
                                 range(COUNT_OF_TESTS['stylish']),
))

TESTS_FOR_PLAIN = list(product(STRUCTURE_TYPES,
                               FILE_TYPES,
                               ['plain'],
                               range(COUNT_OF_TESTS['plain']),
))

TESTS_FOR_JSON = list(product(STRUCTURE_TYPES,
                              FILE_TYPES,
                              ['json'],
                              range(COUNT_OF_TESTS['json']),
))

TEST_COMBINATIONS = TESTS_FOR_STYLISH + TESTS_FOR_PLAIN + TESTS_FOR_JSON
FIXTURES_PATH = 'tests/fixtures'
FORMATTERS_FOLDER = 'formatters'


def get_path_to_fixture(*args):
    return os.path.join(FIXTURES_PATH, *args)


@pytest.mark.parametrize(
    'structure_type, file_type, formatter, test_number',
    TEST_COMBINATIONS
)
def test_generate_diff(structure_type, file_type,
                       formatter, test_number):
    filename1 = f'{TESTS[test_number][TEST_FILE1] }.{file_type}'
    filename2 = f'{TESTS[test_number][TEST_FILE2] }.{file_type}'
    result_filename = TESTS[test_number][RESULT_FILE]

    file1 = get_path_to_fixture(structure_type, file_type, filename1)
    file2 = get_path_to_fixture(structure_type, file_type, filename2)
    result = load(
        get_path_to_fixture(
            structure_type, FORMATTERS_FOLDER,
            formatter, result_filename
        )
    )
    assert generate_diff(file1, file2, formatter) == result
