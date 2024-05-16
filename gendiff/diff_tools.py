def determine_type(value):
    return 'complex' if isinstance(value, dict) else 'simple'


def generate_node(key, value1, value2):
    type1 = determine_type(value1)
    type2 = determine_type(value2)

    status = 'unchanged'
    values = {'values': value1}
    types = {'type': type1}
    if type1 == type2 == 'complex' and value1 != value2:
        status = 'nested'
        values = {'children': build_diff(value1, value2)}
        types = {'type': 'diff'}
    elif value1 is None:
        status = 'added'
        values['values'] = value2
        types = {'type': type2}
    elif value2 is None:
        status = 'removed'
    elif value1 != value2:
        status = 'updated'
        values = {'old_value': value1, 'new_value': value2}
        types = {'old_type': type1,
                 'new_type': type2}
    return {'key': key, 'status': status} | values | types


def build_diff(dict1, dict2):
    diff = []
    for key in sorted(set(dict1) | set(dict2)):
        value1, value2 = dict1.get(key), dict2.get(key)
        diff.append(generate_node(key, value1, value2))
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
