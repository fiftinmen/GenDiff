import pytest
import os
from copy import deepcopy
from gendiff.structured_dicts import (
    structured_dict,
    FILLER_TEMPLATE,
    STATUSES,
    get_status,
    get_value,
    get_key,
    tree,
    DEFAULT_STATUS,
    is_tree,
    find_structured_dict_by_key
)
from gendiff.formatters import plain, json_formatter
import json
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


status_same = STATUSES['same']
status_del = STATUSES['old']
status_new = STATUSES['new']


dictionary1 = {'foo': 'bar'}
dictionary1_copy = deepcopy(dictionary1)
dictionary2 = {'foobar': 'foobar'}
dictionary3 = {'foo': 'foobar'}
dictionary4 = structured_dict(key=key, value=value, status=status_same)
dictionary5 = structured_dict(key=key, value=value, status=status_same)
dictionary6 = {'foo': {'foobar': 'foobar'}}
dictionary7 = {'foo': {'foobar': 'foo'}}
dictionary8 = {'foo': {'foo': 'foo'}}
dictionary9 = {'foo': {'foobar': 'foobar', 'foobar': 'foobar'}}

tree1 = [
    {'key': 'foo', 'value': 'bar', 'status': '-'},
    {'key': 'foo', 'value': 'foobar', 'status': '+'},
    {'key': 'foo1', 'value': 'foobar', 'status': '+'},
    {'key': 'foo1', 'value': 'foobar', 'status': '+'}
]


d1_d3_result = [
    {'key': 'foo', 'value': 'bar', 'status': '-'},
    {'key': 'foo', 'value': 'foobar', 'status': '+'}
]
d1_empty_result = [{'key': 'foo', 'value': 'bar', 'status': '-'}]
empty_d1_result = [{'key': 'foo', 'value': 'bar', 'status': '+'}]
d1_d1_result = [
    {'key': 'foo', 'value': 'bar', 'status': ' '},
]
d1_d6_result = [
    {'key': 'foo', 'value': 'bar', 'status': '-'},
    {'key': 'foo', 'value': [
        {'key': 'foobar', 'value': 'foobar', 'status': ' '},
    ], 'status': '+'},
]
d6_d7_result = [
    {'key': 'foo', 'value': [
        {'key': 'foobar', 'value': 'foobar', 'status': '-'},
        {'key': 'foobar', 'value': 'foo', 'status': '+'},
    ], 'status': ' '
    }
]
d6_d8_result = [
    {'key': 'foo', 'value': [
        {'key': 'foo', 'value': 'foobar', 'status': '-'},
        {'key': 'foo', 'value': 'foo', 'status': '+'},
    ], 'status': ' '},
]
d6_d9_result = [
    {'key': 'foo', 'value': [
        {'key': 'foobar', 'value': 'foobar', 'status': ' '},
        {'key': 'foobar', 'value': 'foobar', 'status': ' '},
    ], 'status': ' '},
]


def test_find_structured_dict_by_key():
    assert find_structured_dict_by_key('foo', tree1, 1) == \
        {'key': 'foo', 'value': 'bar', 'status': '-'}
    assert find_structured_dict_by_key('foo', tree1, 0) == \
        {'key': 'foo', 'value': 'bar', 'status': '-'}
    assert find_structured_dict_by_key('foo', tree1, 5) == [
        {'key': 'foo', 'value': 'bar', 'status': '-'},
        {'key': 'foo', 'value': 'foobar', 'status': '+'}
    ]
    


def test_compare_plain():
    assert compare(dictionary1, dictionary3) == d1_d3_result
    assert compare(dictionary1, {}) == d1_empty_result
    assert compare({}, dictionary1) == empty_d1_result
    assert compare(dictionary1, dictionary1) == d1_d1_result


def test_compare_nested():
    assert compare(dictionary1, dictionary6) == d1_d6_result
    assert compare(dictionary6, dictionary7) == d6_d7_result


def test_is_tree():
    assert is_tree([{'key': 'foo', 'value': 'bar', 'status': ' '}]) is True
    assert is_tree([{'key': 'foo', 'value': 'bar'}]) is True
    assert is_tree([{'key': 'foo', 'bar': 'bar', 'status': ' '}]) is False
    assert is_tree([{'key': 'foo'}]) is False


def test_tree():
    assert tree({'key': 'foo', 'value': 'bar', 'status': ' '}) == {
        'key': 'foo', 'value': 'bar', 'status': ' '}
    assert tree({'aaaa': 'foo', 'value': 'bar'}) == [
        {'key': 'aaaa', 'value': 'foo', 'status': ' '},
        {'key': 'value', 'value': 'bar', 'status': ' '}]
    assert tree({'key': 'aaaa', 'value': {
        'key': 'foo'}, 'status': ' '}) == {
            'key': 'aaaa', 'value': [
                {'key': 'key', 'value': 'foo', 'status': ' '}],
            'status': ' '
    }
    assert tree({'key': 'aaaa', 'value': {
        'key': 'foo'}}, status='-') == {
            'key': 'aaaa', 'value': [
                {'key': 'key', 'value': 'foo', 'status': ' '}
            ], 'status': '-'}
    return


def test_getters():
    assert get_status(dictionary4, status_new) == status_same
    assert get_key(dictionary4) == key
    assert get_value(dictionary4) == value

    assert get_status(dictionary3) is None
    assert get_key(dictionary3) == 'foo'
    assert get_value(dictionary3) is None
    assert get_value(dictionary3, 'foo') == 'foobar'

    assert get_value(None) is None
    assert get_status(None) == DEFAULT_STATUS
    assert get_key(None) is None


def test_structured_dict():
    assert structured_dict(key1, value1) == {
        'key': key1, 'value': value1, 'status': ' '
    }
    assert structured_dict(key1, {'foo': 'bar'}) == {
        'key': key1, 'value': {'foo': 'bar'}, 'status': ' '
    }
    assert structured_dict(key1, {'key': 'foo', 'value': 'bar'}) == {
        'key': key1, 'value': {'key': 'foo', 'value': 'bar'}, 'status': ' '
    }
    assert structured_dict(
        key1, {'key': 'foo', 'value': 'bar', 'status': 'new'}) == {
        'key': key1, 'value': {'key': 'foo', 'value': 'bar', 'status': 'new'},
        'status': ' '
    }
    assert structured_dict(
        key1, {'key': 'foo', 'value': 'bar', 'status': 'new'}, 'new') == {
        'key': key1, 'value': {'key': 'foo',
                               'value': 'bar', 'status': 'new'}, 'status': 'new'
    }
    assert structured_dict(None, None, None) == {
        'key': None, 'value': None, 'status': None
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


def test_compare_neste_with_plain_formatter():
    result_diff_path = os.path.join(fixtures_path, 'result_plain.txt')
    result_diffs = open(result_diff_path, 'r', encoding='utf8').read()
    file1 = os.path.join(fixtures_path, 'nested_jsons/file1.json')
    file2 = os.path.join(fixtures_path, 'nested_jsons/file2.json')
    assert generate_diff(file1, file2, formatter=plain) == result_diffs


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


def test_generate_diff_from_nested_jsons_with_json_formatter():
    file1 = os.path.join(fixtures_path, 'nested_jsons/file1.json')
    file2 = os.path.join(fixtures_path, 'nested_jsons/file2.json')
    assert generate_diff(file1, file2, formatter=json_formatter)


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
