from math import inf
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


def is_atomic_dict(value):
    if not is_dict(value) or len(value) < 2 or len(value) > 3:
        return False
    for key in value.keys():
        if key not in ['key', 'value', 'sign']:
            return False
    return True


def get_atomic_dict(key1, dict_list):
    for dictionary in dict_list:
        key2 = get_key(dictionary)
        if is_atomic_dict(dictionary) and key1 == key2:
            return dictionary
    return None


def get_key(dictionary):
    if is_dict(dictionary):
        key = dictionary.get('key')
        if key:
            return key
        elif len(dictionary) == 1:
            return format(list(dictionary.keys())[0])
    return format(dictionary)


def get_value(dictionary, key=None, default=None):
    if is_dict(dictionary):
        if key is None:
            return dictionary.get('value')
        else:
            return dictionary.get(key)
    return default


def get_sign(dictionary, default=DEFAULT_SIGN):
    if is_dict(dictionary):
        sign = dictionary.get('sign')
        return sign
    return default


def set_key(atom, key):
    atom.update({'key': key})


def set_value(atom, value):
    atom.update({'value': value})


def set_sign(atom, sign):
    atom.update({'sign': sign})


def atomic_dict(key, value, sign=DEFAULT_SIGN):
    atom = {}
    set_key(atom, key)
    set_value(atom, value)
    set_sign(atom, sign)
    return atom


def nested_dict(object, sign=DEFAULT_SIGN):
    if is_list(object):
        result = []
        for element in object:
            result.append(nested_dict(element, sign))
        return result
    if not is_dict(object):
        return object
    elif is_atomic_dict(object):
        value = get_value(object)
        value = nested_dict(value)
        set_value(object, value)
        set_sign(object, sign)
        return object
    else:
        result = []
        for key, value in object.items():
            new_dict = atomic_dict(key, nested_dict(value), sign)
            result.append(new_dict)
        return result


def is_list(object):
    return isinstance(object, list)


def is_nested_dict(object):
    if not is_list(object):
        return False
    elif is_list(object):
        for item in object:
            if not is_atomic_dict(item):
                return False
    return True


def get_atoms(nested_dict):
    for atom in nested_dict:
        yield atom


def sort_nested_dict(object):
    if is_nested_dict(object):
        object.sort(key=sort_nested_dict)
        return inf
    if is_atomic_dict(object):
        value = get_value(object)
        if is_nested_dict(value):
            value.sort(key=sort_nested_dict)
        return get_key(object)
