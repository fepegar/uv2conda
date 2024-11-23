from packaging.version import InvalidVersion
from packaging.version import Version


def is_valid_python_version(version: str) -> bool:
    """
    Checks if a string is a valid Python version using the packaging library.

    Args:
        version: The version string to validate.

    Returns:
        bool: True if the version is valid, False otherwise.
    """
    try:
        Version(version)
        return True
    except InvalidVersion:
        return False
