from math import inf
from copy import deepcopy
SIGNS = {
    'same': ' ',
    'old': '-',
    'new': '+'
}
DEFAULT_SIGN = SIGNS['same']
DEFAULT_LEVEL = 1
FILLER_TEMPLATE = '  '


def is_dict(value):
    return isinstance(value, dict)


def is_valid_structured_dict(value):
    if not is_dict(value) or len(value) < 2 or len(value) > 3:
        return False
    return all(key in ['key', 'value', 'sign'] for key in value.keys())


def find_structured_dict_by_key(key1, dict_list, number=1):
    result = []
    for dictionary in dict_list:
        key2 = get_key(dictionary)
        if is_valid_structured_dict(dictionary) and key1 == key2:
            if number < 2:
                return dictionary
            result.append(dictionary)
            if len(result) == number:
                return result
    return None or result


def get_key(dictionary):
    if is_dict(dictionary):
        if key := dictionary.get('key'):
            return key
        elif len(dictionary) == 1:
            return list(dictionary.keys())[0]
    return dictionary


def get_value(dictionary, key=None, default=None):
    if is_dict(dictionary):
        return dictionary.get('value') if key is None else dictionary.get(key)
    return default


def get_sign(dictionary, default=DEFAULT_SIGN):
    return dictionary.get('sign') if is_dict(dictionary) else default


def set_key(atom, key):
    atom.update({'key': key})


def set_value(atom, value):
    atom.update({'value': value})


def set_sign(atom, sign):
    atom.update({'sign': sign})


def structured_dict(key, value, sign=DEFAULT_SIGN):
    atom = {}
    set_key(atom, key)
    set_value(atom, value)
    set_sign(atom, sign)
    return atom


def nested_dict(object, sign=DEFAULT_SIGN):
    if is_nested_dict(object):
        return [nested_dict(element, sign) for element in object]
    if not is_dict(object):
        return object
    elif is_valid_structured_dict(object):
        value = get_value(object)
        value = nested_dict(value)
        set_value(object, value)
        set_sign(object, sign)
        return object
    else:
        result = []
        for key, value in object.items():
            new_dict = structured_dict(key, nested_dict(value), sign)
            result.append(new_dict)
        return result


def is_list(object):
    return isinstance(object, list)


def is_nested_dict(object):
    if not is_list(object):
        return False
    elif is_list(object):
        for item in object:
            if not is_valid_structured_dict(item):
                return False
    return True


def yield_nested_dict_items(nested_dict):
    yield from nested_dict


def extract_changes_from_nested_dict_items(nested_dict, parent=None):
    changed_properties = []
    nested_dict_copy = deepcopy(nested_dict)
    keys = set()
    for struct_dict in yield_nested_dict_items(nested_dict_copy):
        key = get_key(struct_dict)
        if key in keys:
            continue
        keys.add(key)
        sign = get_sign(struct_dict)
        if sign != SIGNS['same']:
            changed_dicts = find_structured_dict_by_key(
                key, nested_dict, number=2
            )
            for changed_dict in changed_dicts:
                set_key(changed_dict, f'{parent}.{key}' if parent else key)
            changed_properties.append(changed_dicts)
        else:
            value = get_value(struct_dict)
            if is_nested_dict(value):
                child_changes = extract_changes_from_nested_dict_items(
                    value,
                    parent=f'{parent}.{key}' if parent else key
                )
                changed_properties.extend(child_changes)
    return changed_properties


def yield_changes_from_nested_dict_items(nested_dict):
    yield from extract_changes_from_nested_dict_items(nested_dict)


def sort_nested_dict(object):
    if is_nested_dict(object):
        object.sort(key=sort_nested_dict)
        return inf
    if is_valid_structured_dict(object):
        value = get_value(object)
        if is_nested_dict(value):
            value.sort(key=sort_nested_dict)
        return get_key(object)
