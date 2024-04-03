import pytest
from copy import deepcopy
from gendiff.scripts.gendiff import (
    get_item_difference,
    generate_line,
    generate_diff,
    FILLER_TEMPLATE,
    SIGNS
)

key = 'foo'
value = 'bar'
key1 = 'foooo'
value1 = 'foobar'
empty_key = None
empty_value = None
number_key = 1
number_value = 1
bool_key = True
bool_value = False

dictionary1 = {'foo': 'bar'}
dictionary1_copy = deepcopy(dictionary1)
dictionary2 = {'foobar': 'foobar'}
dictionary3 = {'foo': 'foobar'}

list1 = [{'foo': 'bar'}]

filler = FILLER_TEMPLATE
filler1 = '!'

sign_equal = SIGNS['equal']
sign_not_equal = SIGNS['not equal']
sign_new = SIGNS['new']


def test_generate_line():
    assert generate_line(key, value) == f"{filler}{sign_equal} {key}: {value}"
    assert generate_line(key, value, sign=sign_not_equal) ==\
        f"{filler}{sign_not_equal} {key}: {value}"
    assert generate_line(key, value, sign=sign_not_equal, filler=filler1) ==\
        f"{filler1}{sign_not_equal} {key}: {value}"
    assert generate_line(key, value, filler=filler1) ==\
        f"{filler1}{sign_equal} {key}: {value}"
    assert generate_line(number_key, number_value, filler=filler1) ==\
        f"{filler1}{sign_equal} {str(number_key)}: {str(number_value)}"


def test_get_item_difference():
    result1 = [f'{filler}{sign_equal} {key}: {value}']
    assert get_item_difference(key, value, {key: value}) == result1
    assert dictionary1 == dictionary1_copy

    result2 = [
        f'{filler}{sign_not_equal} {key}: {value}',
        f'{filler}{sign_new} {key}: {value1}'
    ]
    assert get_item_difference(key, value, {key: value1}) == result2

    result3 = [
        f'{filler}{sign_new} {key1}: {value1}'
    ]
    assert get_item_difference(key1, value1,
                               {key: value}, diff=result2) == result3

    result3 = [f'{filler}{sign_not_equal} {key}: {value}']
    assert get_item_difference(key, value, {key1: value1}) == result3


file1 = 'tests/file1.json'
file2 = 'tests/file2.json'
file3 = 'tests/file3.json'
result_diffs1 = open('tests/result_diffs1.txt', 'r', encoding='utf8').read()
result_diffs2 = open('tests/result_diffs2.txt', 'r', encoding='utf8').read()
result_diffs3 = open('tests/result_diffs3.txt', 'r', encoding='utf8').read()
result_diffs4 = open('tests/result_diffs4.txt', 'r', encoding='utf8').read()


def test_generate_diff():
    assert generate_diff(file1, file2) == result_diffs1
    assert generate_diff(file1, file1) == result_diffs2
    assert generate_diff(file1, file3) == result_diffs3
    assert generate_diff(file3, file1) == result_diffs4
