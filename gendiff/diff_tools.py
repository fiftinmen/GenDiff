def build_diff(dict1, dict2):
    diff = []
    keys1 = set(dict1)
    keys2 = set(dict2)
    keys = sorted(keys1 | keys2)
    for key in keys:
        value1, value2 = dict1.get(key), dict2.get(key)
        status = 'unchanged'
        value = {'value': value1}
        if isinstance(value1,
                      dict) and isinstance(value2, dict) and value1 != value2:
            status = 'nested'
            value = {'children': build_diff(value1, value2)}
        elif key not in keys1:
            status = 'added'
            value['value'] = value2
        elif key not in keys2:
            status = 'removed'
        elif value1 != value2:
            status = 'updated'
            value = {'old_value': value1, 'new_value': value2}
        diff.append({'key': key, 'status': status} | value)
    return diff


def get_key(node):
    return node.get('key')


def get_status(node):
    return node.get('status')


def get_value(node):
    status = get_status(node)
    if status == 'nested':
        return node.get('children')
    if status == 'updated':
        return node.get('old_value'), node.get('new_value')
    else:
        return node.get('value')
