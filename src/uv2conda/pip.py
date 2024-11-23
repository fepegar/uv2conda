from .types import TypePath


def read_requirements_file(requirements_file: TypePath) -> list[str]:
    """Read a requirements file and return a list of requirements.

    Removes comments and empty lines.

    Args:
        requirements_file: Path to the requirements file.
    """
    with open(requirements_file) as f:
        lines = f.readlines()
    requirements = []
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        requirements.append(line)
    return requirements
