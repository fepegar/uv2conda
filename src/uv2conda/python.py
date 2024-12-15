from pathlib import Path

from packaging.version import InvalidVersion
from packaging.version import Version


def is_valid_python_version(version: str) -> bool:
    """Check if a string is a valid Python version.

    Args:
        version: The version string to validate.

    Returns:
        bool: True if the version is valid, False otherwise.

    Raises:
        InvalidVersion: If the version string is not a valid version.
    """
    try:
        Version(version)
    except InvalidVersion:
        return False
    else:
        return True


def check_python_version(python_version: str) -> None:
    if not is_valid_python_version(python_version):
        msg = f'Invalid Python version: "{python_version}"'
        raise ValueError(msg)


def get_python_version_from_project_dir(project_dir: Path) -> str | None:
    """Get the Python version from the project directory.

    This function looks for a file named `.python-version` in the project
    directory and returns the version specified in that file. If the file
    does not exist, it returns None.

    Args:
        project_dir: The project directory.

    Returns:
        str | None: The Python version or None if not found.
    """
    pinned_version_path = project_dir / ".python-version"
    if pinned_version_path.exists():
        return pinned_version_path.read_text().strip()
    else:
        return None
