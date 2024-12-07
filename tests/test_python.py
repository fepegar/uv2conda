from uv2conda.python import is_valid_python_version


def test_valid_python_versions():
    assert is_valid_python_version("3")
    assert is_valid_python_version("2.7")
    assert is_valid_python_version("3.9.1")


def test_invalid_python_versions():
    assert not is_valid_python_version("x")
    assert not is_valid_python_version("three.eight.zero")
    assert not is_valid_python_version("")
