import gendiff


def test_names():
    assert hasattr(gendiff, 'generate_diff')
    assert hasattr(gendiff, 'compare_dicts')
    assert not hasattr(gendiff, 'get_key')
