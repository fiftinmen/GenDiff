def determine_type(value):
    return 'complex' if isinstance(value, dict) else 'simple'


def build_diff(dict1, dict2):
    diff = []
    keys1 = set(dict1)
    keys2 = set(dict2)
    keys = sorted(keys1 | keys2)
    for key in keys:
        value1, value2 = dict1.get(key), dict2.get(key)
        type1 = determine_type(value1)
        type2 = determine_type(value2)

        status = 'unchanged'
        values = {'values': value1}
        types = {'type': type1}
        if type1 == type2 == 'complex' and value1 != value2:
            status = 'nested'
            values = {'children': build_diff(value1, value2)}
            types = {'type': 'diff'}
        elif key not in keys1:
            status = 'added'
            values['values'] = value2
            types = {'type': type2}
        elif key not in keys2:
            status = 'removed'
        elif value1 != value2:
            status = 'updated'
            values = {'old_value': value1, 'new_value': value2}
            types = {'old_type': type1,
                     'new_type': type2}
        diff.append({'key': key, 'status': status} | values | types)
    return diff


def get_key(node):
    return node.get('key')


def get_status(node):
    return node.get('status')


def get_values(node):
    status = get_status(node)
    if status == 'nested':
        return node.get('children')
    if status == 'updated':
        return node.get('old_value'), node.get('new_value')
    else:
        return node.get('values')


def get_values_types(node):
    status = get_status(node)
    return (node.get('old_type'), node.get('new_type')) if status == 'updated' \
        else node.get('type')
