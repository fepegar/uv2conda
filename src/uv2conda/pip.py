from pathlib import Path


def read_requirements_file(requirements_file: Path) -> list[str]:
    """Read a requirements file and return a list of requirements.

    Removes comments and empty lines.

    Args:
        requirements_file: Path to the requirements file.

    """
    with requirements_file.open() as f:
        lines = f.readlines()
    requirements = []
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        requirements.append(stripped)
    return requirements
