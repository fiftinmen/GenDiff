import pytest
import os
from copy import deepcopy
from gendiff.scripts.gendiff_parser.gendiff_parser import (
    get_item_difference,
    generate_line,
    generate_diff,
    is_new_key,
    generate_dictionary,
    FILLER_TEMPLATE,
    SIGNS,
    get_sign,
    get_filler,
    get_value,
    get_key,
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


list1 = [{'foo': 'bar'}]


filler = FILLER_TEMPLATE
filler1 = '!'


sign_same = SIGNS['same']
sign_del = SIGNS['del']
sign_new = SIGNS['new']


dictionary1 = {'foo': 'bar'}
dictionary1_copy = deepcopy(dictionary1)
dictionary2 = {'foobar': 'foobar'}
dictionary3 = {'foo': 'foobar'}
dictionary4 = generate_dictionary(key=key, value=value,
                                  sign=sign_same, filler=filler)


def test_getters():
    assert get_sign(dictionary4, sign_new) == sign_same
    assert get_key(dictionary4) == key
    assert get_value(dictionary4) == value
    assert get_filler(dictionary4) == filler

    assert get_sign(dictionary3) == sign_same
    assert get_key(dictionary3) == 'foo'
    assert get_value(dictionary3) is None
    assert get_value(dictionary3, 'foo') == 'foobar'
    assert get_filler(dictionary3) == FILLER_TEMPLATE


def test_generate_line():
    assert generate_line(key, value) == f"{filler}{sign_same} {key}: {value}"
    assert generate_line(key, value, sign=sign_del) ==\
        f"{filler}{sign_del} {key}: {value}"
    assert generate_line(key, value, sign=sign_del, filler=filler1) ==\
        f"{filler1}{sign_del} {key}: {value}"
    assert generate_line(key, value, filler=filler1) ==\
        f"{filler1}{sign_same} {key}: {value}"
    assert generate_line(number_key, number_value, filler=filler1) ==\
        f"{filler1}{sign_same} {str(number_key)}: {str(number_value)}"


def test_generate_dictionary():
    assert generate_dictionary(key1, value1, sign_new, filler1) == dict(
        [['key', key1], ['value', value1],
         ['sign', sign_new], ['filler', filler1]])
    assert generate_dictionary(key1, value1) == dict(
        [['key', key1], ['value', value1],
         ['sign', sign_same], ['filler', FILLER_TEMPLATE]])


def test_get_item_difference():
    result1 = [generate_dictionary(key, value)]
    assert get_item_difference(key, value, {key: value}) == result1

    result2 = [
        generate_dictionary(key, value, sign_del, filler1),
        generate_dictionary(key, value1, sign_new, filler1),
    ]
    assert get_item_difference(key, value,
                               {key: value1}, filler=filler1) == result2

    result3 = [generate_dictionary(key, value, sign_del)]
    assert get_item_difference(key, value, {key1: value1}) == result3
    result3 = [generate_dictionary(key, value, sign_del)]
    assert get_item_difference(key, value, {}) == result3


fixtures_path = 'tests/fixtures'
result_diff1_path = os.path.join(fixtures_path, 'result_diffs1.txt')
result_diff2_path = os.path.join(fixtures_path, 'result_diffs2.txt')
result_diff3_path = os.path.join(fixtures_path, 'result_diffs3.txt')
result_diff4_path = os.path.join(fixtures_path, 'result_diffs4.txt')
result_diffs1 = open(result_diff1_path, 'r', encoding='utf8').read()
result_diffs2 = open(result_diff2_path, 'r', encoding='utf8').read()
result_diffs3 = open(result_diff3_path, 'r', encoding='utf8').read()
result_diffs4 = open(result_diff4_path, 'r', encoding='utf8').read()


def test_generate_diff_from_jsons():
    file1 = os.path.join(fixtures_path, 'file1.json')
    file2 = os.path.join(fixtures_path, 'file2.json')
    file3 = os.path.join(fixtures_path, 'file3.json')
    assert generate_diff(file1, file2) == result_diffs1
    assert generate_diff(file1, file1) == result_diffs2
    assert generate_diff(file1, file3) == result_diffs3
    assert generate_diff(file3, file1) == result_diffs4


def test_generate_diff_from_yamls():
    file1 = os.path.join(fixtures_path, 'file1.yml')
    file2 = os.path.join(fixtures_path, 'file2.yaml')
    file3 = os.path.join(fixtures_path, 'file3.yml')
    assert generate_diff(file1, file2) == result_diffs1
    assert generate_diff(file1, file1) == result_diffs2
    assert generate_diff(file1, file3) == result_diffs3
    assert generate_diff(file3, file1) == result_diffs4


def test_is_new_key():
    assert is_new_key(value, [{'key': value}]) is False
    assert is_new_key(value, [{'key': value1}]) is True
    assert is_new_key(value, [{'key': value1}, {'key': value}]) is False
    assert is_new_key(value, [{}]) is True
    assert is_new_key(value, [{'mouse': value}]) is True
