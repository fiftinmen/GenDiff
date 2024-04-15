from math import inf
from copy import deepcopy
STATUSES = {
    'same': ' ',
    'old': '-',
    'new': '+'
}
DEFAULT_STATUS = STATUSES['same']
DEFAULT_LEVEL = 1
FILLER_TEMPLATE = '  '


def is_dict(value):
    return isinstance(value, dict)


def is_valid_structured_dict(value):
    if not is_dict(value) or len(value) < 2 or len(value) > 3:
        return False
    return all(key in ['key', 'value', 'status'] for key in value.keys())


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


def get_status(dictionary, default=DEFAULT_STATUS):
    return dictionary.get('status') if is_dict(dictionary) else default


def set_key(atom, key):
    atom.update({'key': key})


def set_value(atom, value):
    atom.update({'value': value})


def set_status(atom, status):
    atom.update({'status': status})


def structured_dict(key, value, status=DEFAULT_STATUS):
    atom = {}
    set_key(atom, key)
    set_value(atom, value)
    set_status(atom, status)
    return atom


def tree(object, status=DEFAULT_STATUS):
    if is_tree(object):
        return [tree(element, status) for element in object]
    if not is_dict(object):
        return object
    elif is_valid_structured_dict(object):
        value = get_value(object)
        value = tree(value)
        set_value(object, value)
        set_status(object, status)
        return object
    else:
        result = []
        for key, value in object.items():
            new_dict = structured_dict(key, tree(value), status)
            result.append(new_dict)
        return result


def is_list(object):
    return isinstance(object, list)


def is_tree(object):
    if not is_list(object):
        return False
    elif is_list(object):
        for item in object:
            if not is_valid_structured_dict(item):
                return False
    return True


def yield_tree_items(tree):
    yield from tree


def extract_changes_from_tree_items(tree, parent=None):
    changed_properties = []
    tree_copy = deepcopy(tree)
    keys = set()
    for struct_dict in yield_tree_items(tree_copy):
        key = get_key(struct_dict)
        if key in keys:
            continue
        keys.add(key)
        status = get_status(struct_dict)
        if status != STATUSES['same']:
            changed_dicts = find_structured_dict_by_key(
                key, tree, number=2
            )
            for changed_dict in changed_dicts:
                set_key(changed_dict, f'{parent}.{key}' if parent else key)
            changed_properties.append(changed_dicts)
        else:
            value = get_value(struct_dict)
            if is_tree(value):
                child_changes = extract_changes_from_tree_items(
                    value,
                    parent=f'{parent}.{key}' if parent else key
                )
                changed_properties.extend(child_changes)
    return changed_properties


def yield_changes_from_tree_items(tree):
    yield from extract_changes_from_tree_items(tree)


def sort_tree(object):
    if is_tree(object):
        object.sort(key=sort_tree)
        return inf
    if is_valid_structured_dict(object):
        value = get_value(object)
        if is_tree(value):
            value.sort(key=sort_tree)
        return get_key(object)
