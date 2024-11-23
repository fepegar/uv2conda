import subprocess
import tempfile
from typing import Optional

from .pip import read_requirements_file
from .types import TypePath


def write_requirements_file_from_uv_project(
    project_dir: TypePath,
    out_path: TypePath,
    extra_args: Optional[list[str]] = None,
) -> None:
    command = [
        "uv",
        "export",
        "--project", str(project_dir),
        "--no-emit-project",
        "--no-dev",
        "--no-hashes",
        "--quiet",
        "--output-file", str(out_path),
    ]
    if extra_args is not None:
        command.extend(extra_args)
    subprocess.run(command, check=True)


def get_requirents_from_uv_project(project_dir: TypePath) -> list[str]:
    with tempfile.NamedTemporaryFile(mode="w") as f:
        write_requirements_file_from_uv_project(project_dir, f.name)
        return read_requirements_file(f.name)
