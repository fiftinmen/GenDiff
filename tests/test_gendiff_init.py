import gendiff


def test_names():
    assert hasattr(gendiff, 'generate_diff')
    assert hasattr(gendiff, 'compare')
    assert not hasattr(gendiff, 'get_key')
