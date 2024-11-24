import subprocess
import tempfile
from typing import Optional

from .pip import read_requirements_file
from .types import TypePath


def write_requirements_file_from_project_dir(
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
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        msg = f"Failed to write requirements file from uv project: {e}"
        raise RuntimeError(msg) from e


def get_requirents_from_project_dir(
    project_dir: TypePath,
    uv_args: Optional[list[str]] = None,
) -> list[str]:
    with tempfile.NamedTemporaryFile(mode="w") as f:
        write_requirements_file_from_project_dir(
            project_dir,
            f.name,
            extra_args=uv_args,
        )
        return read_requirements_file(f.name)
