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
