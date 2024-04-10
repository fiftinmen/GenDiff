import pytest
import os
from copy import deepcopy
from gendiff.atomic_dicts import (
    atomic_dict,
    FILLER_TEMPLATE,
    SIGNS,
    get_sign,
    get_value,
    get_key,
    nested_dict,
    DEFAULT_SIGN,
    is_nested_dict
)
from gendiff.scripts.gendiff_parser.gendiff_parser import (
    generate_diff,
    compare
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
sign_del = SIGNS['old']
sign_new = SIGNS['new']


dictionary1 = {'foo': 'bar'}
dictionary1_copy = deepcopy(dictionary1)
dictionary2 = {'foobar': 'foobar'}
dictionary3 = {'foo': 'foobar'}
dictionary4 = atomic_dict(key=key, value=value, sign=sign_same)
dictionary5 = atomic_dict(key=key, value=value, sign=sign_same)
dictionary6 = {'foo': {'foobar': 'foobar'}}
dictionary7 = {'foo': {'foobar': 'foo'}}
dictionary8 = {'foo': {'foo': 'foo'}}
dictionary9 = {'foo': {'foobar': 'foobar', 'foobar': 'foobar'}}


d1_d3_result = [
    {'key': 'foo', 'value': 'bar', 'sign': '-'},
    {'key': 'foo', 'value': 'foobar', 'sign': '+'}
]
d1_empty_result = [{'key': 'foo', 'value': 'bar', 'sign': '-'}]
empty_d1_result = [{'key': 'foo', 'value': 'bar', 'sign': '+'}]
d1_d1_result = [
    {'key': 'foo', 'value': 'bar', 'sign': ' '},
]
d1_d6_result = [
    {'key': 'foo', 'value': 'bar', 'sign': '-'},
    {'key': 'foo', 'value': [
        {'key': 'foobar', 'value': 'foobar', 'sign': ' '},
    ], 'sign': '+'},
]
d6_d7_result = [
    {'key': 'foo', 'value': [
        {'key': 'foobar', 'value': 'foobar', 'sign': '-'},
        {'key': 'foobar', 'value': 'foo', 'sign': '+'},
    ], 'sign': ' '
    }
]
d6_d8_result = [
    {'key': 'foo', 'value': [
        {'key': 'foo', 'value': 'foobar', 'sign': '-'},
        {'key': 'foo', 'value': 'foo', 'sign': '+'},
    ], 'sign': ' '},
]
d6_d9_result = [
    {'key': 'foo', 'value': [
        {'key': 'foobar', 'value': 'foobar', 'sign': ' '},
        {'key': 'foobar', 'value': 'foobar', 'sign': ' '},
    ], 'sign': ' '},
]


def test_compare_plain():
    assert compare(dictionary1, dictionary3) == d1_d3_result
    assert compare(dictionary1, {}) == d1_empty_result
    assert compare({}, dictionary1) == empty_d1_result
    assert compare(dictionary1, dictionary1) == d1_d1_result


def test_compare_nested():
    assert compare(dictionary1, dictionary6) == d1_d6_result
    assert compare(dictionary6, dictionary7) == d6_d7_result


def test_is_nested_dict():
    assert is_nested_dict([{'key': 'foo', 'value': 'bar', 'sign': ' '}]) is True
    assert is_nested_dict([{'key': 'foo', 'value': 'bar'}]) is True
    assert is_nested_dict([{'key': 'foo', 'bar': 'bar', 'sign': ' '}]) is False
    assert is_nested_dict([{'key': 'foo'}]) is False


def test_nested_dict():
    assert nested_dict({'key': 'foo', 'value': 'bar', 'sign': ' '}) == {
        'key': 'foo', 'value': 'bar', 'sign': ' '}
    assert nested_dict({'aaaa': 'foo', 'value': 'bar'}) == [
        {'key': 'aaaa', 'value': 'foo', 'sign': ' '},
        {'key': 'value', 'value': 'bar', 'sign': ' '}]
    assert nested_dict({'key': 'aaaa', 'value': {
        'key': 'foo'}, 'sign': ' '}) == {
            'key': 'aaaa', 'value': [
                {'key': 'key', 'value': 'foo', 'sign': ' '}],
            'sign': ' '
    }
    assert nested_dict({'key': 'aaaa', 'value': {
        'key': 'foo'}}, sign='-') == {
            'key': 'aaaa', 'value': [
                {'key': 'key', 'value': 'foo', 'sign': ' '}
            ], 'sign': '-'}
    return


def test_getters():
    assert get_sign(dictionary4, sign_new) == sign_same
    assert get_key(dictionary4) == key
    assert get_value(dictionary4) == value

    assert get_sign(dictionary3) is None
    assert get_key(dictionary3) == 'foo'
    assert get_value(dictionary3) is None
    assert get_value(dictionary3, 'foo') == 'foobar'

    assert get_value(None) is None
    assert get_sign(None) == DEFAULT_SIGN
    assert get_key(None) == 'None'


def test_atomic_dict():
    assert atomic_dict(key1, value1) == {
        'key': key1, 'value': value1, 'sign': ' '
    }
    assert atomic_dict(key1, {'foo': 'bar'}) == {
        'key': key1, 'value': {'foo': 'bar'}, 'sign': ' '
    }
    assert atomic_dict(key1, {'key': 'foo', 'value': 'bar'}) == {
        'key': key1, 'value': {'key': 'foo', 'value': 'bar'}, 'sign': ' '
    }
    assert atomic_dict(
        key1, {'key': 'foo', 'value': 'bar', 'sign': 'new'}) == {
        'key': key1, 'value': {'key': 'foo', 'value': 'bar', 'sign': 'new'},
        'sign': ' '
    }
    assert atomic_dict(
        key1, {'key': 'foo', 'value': 'bar', 'sign': 'new'}, 'new') == {
        'key': key1, 'value': {'key': 'foo',
                               'value': 'bar', 'sign': 'new'}, 'sign': 'new'
    }
    assert atomic_dict(None, None, None) == {
        'key': None, 'value': None, 'sign': None
    }


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


result_diff1_path = os.path.join(fixtures_path,
                                     'nested_jsons/result_diffs1.txt')
result_diff2_path = os.path.join(fixtures_path,
                                    'nested_jsons/result_diffs2.txt')
result_diff3_path = os.path.join(fixtures_path,
                                    'nested_jsons/result_diffs3.txt')
result_diff4_path = os.path.join(fixtures_path,
                                     'nested_jsons/result_diffs4.txt')


def test_generate_diff_from_nested_jsons():
    file1 = os.path.join(fixtures_path, 'nested_jsons/file1.json')
    file2 = os.path.join(fixtures_path, 'nested_jsons/file2.json')
    file3 = os.path.join(fixtures_path, 'file3.json')
    
    result_diffs1 = open(result_diff1_path, 'r', encoding='utf8').read()
    result_diffs2 = open(result_diff2_path, 'r', encoding='utf8').read()
    result_diffs3 = open(result_diff3_path, 'r', encoding='utf8').read()
    result_diffs4 = open(result_diff4_path, 'r', encoding='utf8').read()
    assert generate_diff(file1, file2) == result_diffs1
    assert generate_diff(file1, file1) == result_diffs2
    assert generate_diff(file1, file3) == result_diffs3
    assert generate_diff(file3, file1) == result_diffs4


def test_generate_diff_from_nested_yamls():
    file1 = os.path.join(fixtures_path, 'nested_yamls/file1.yaml')
    file2 = os.path.join(fixtures_path, 'nested_yamls/file2.yaml')
    file3 = os.path.join(fixtures_path, 'file3.yml')

    result_diffs1 = open(result_diff1_path, 'r', encoding='utf8').read()
    result_diffs2 = open(result_diff2_path, 'r', encoding='utf8').read()
    result_diffs3 = open(result_diff3_path, 'r', encoding='utf8').read()
    result_diffs4 = open(result_diff4_path, 'r', encoding='utf8').read()
    assert generate_diff(file1, file2) == result_diffs1
    assert generate_diff(file1, file1) == result_diffs2
    assert generate_diff(file1, file3) == result_diffs3
    assert generate_diff(file3, file1) == result_diffs4
