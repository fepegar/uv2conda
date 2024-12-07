from packaging.version import InvalidVersion
from packaging.version import Version


def is_valid_python_version(version: str) -> bool:
    """Check if a string is a valid Python version.

    Args:
        version: The version string to validate.

    Returns:
        bool: True if the version is valid, False otherwise.

    """
    try:
        Version(version)
    except InvalidVersion:
        return False
    else:
        return True
