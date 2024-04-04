import gendiff.scripts


def test_names():
    assert hasattr(gendiff, 'generate_diff')
    assert hasattr(gendiff, 'compare_jsons')
    assert not hasattr(gendiff, 'get_key')
