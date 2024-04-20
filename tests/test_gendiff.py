import pytest
import os
from itertools import product
from gendiff.scripts.gendiff_parser.gendiff_parser import (
    generate_diff,
    FORMATTERS
)

STRUCTURE_TYPES = ['plain_', 'nested']
FILE_TYPES = ['json']
FORMATTER_ = ['stylish', 'plain']
TESTS = [['file1', 'file2', 'result_diffs1.txt'],
         ['file1', 'file1', 'result_diffs2.txt'],
         ['file1', 'file3', 'result_diffs3.txt'],
         ['file3', 'file1', 'result_diffs4.txt']]
TEST_FILE1 = 0
TEST_FILE2 = 1
RESULT_FILE = 2
COUNT_OF_TESTS = {'stylish': 4, 'plain': 1}
TESTS_FOR_STYLISH = product(STRUCTURE_TYPES, FILE_TYPES, ['stylish'],
                            range(COUNT_OF_TESTS['stylish']))
TESTS_FOR_PLAIN = product(STRUCTURE_TYPES, FILE_TYPES, ['plain'],
                          range(COUNT_OF_TESTS['plain']))
TEST_COMBINATIONS = list(TESTS_FOR_STYLISH) + list(TESTS_FOR_PLAIN)
FIXTURES_PATH = 'tests/fixtures'


@pytest.mark.parametrize('structure_type, file_type, formatter, test_number',
                         TEST_COMBINATIONS)
def test_generate_diff_from_jsons(structure_type, file_type, formatter,
                                  test_number):
    filename1 = TESTS[test_number][TEST_FILE1]
    filename2 = TESTS[test_number][TEST_FILE2]
    result_filename = TESTS[test_number][RESULT_FILE]

    file1 = os.path.join(FIXTURES_PATH, structure_type,
                         file_type, f'{filename1}.{file_type}')
    file2 = os.path.join(FIXTURES_PATH, structure_type,
                         file_type, f'{filename2}.{file_type}')
    result_diff1_path = os.path.join(FIXTURES_PATH,
                                     structure_type, formatter,
                                     result_filename)
    result = open(result_diff1_path, 'r', encoding='utf8').read().strip()

    assert generate_diff(file1, file2, FORMATTERS[formatter]) == result
