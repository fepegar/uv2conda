import shutil
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
    _check_uv_installed()
    command = [
        "uv",
        "export",
        "--project",
        project_dir,
        "--no-emit-project",
        "--no-dev",
        "--no-hashes",
        "--quiet",
        "--output-file",
        out_path,
    ]
    if extra_args is not None:
        command.extend(extra_args)
    command = [str(arg) for arg in command]

    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        command_str = " ".join(command)
        msg = (
            "Error creating requirements file from uv project."
            f"\nCommand: {command_str}"
            f"\nOutput: {result.stderr}"
        )
        raise RuntimeError(msg)


def get_requirents_from_project_dir(
    project_dir: TypePath,
    uv_args: Optional[list[str]] = None,
    out_requirements_path: Optional[TypePath] = None,
) -> list[str]:
    if out_requirements_path is None:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt") as f:
            write_requirements_file_from_project_dir(
                project_dir,
                f.name,
                extra_args=uv_args,
            )
            requirements = read_requirements_file(f.name)
    else:
        write_requirements_file_from_project_dir(
            project_dir,
            out_requirements_path,
            extra_args=uv_args,
        )
        requirements = read_requirements_file(out_requirements_path)
    return requirements


def _check_uv_installed() -> None:
    if shutil.which("uv") is None:
        url = "https://docs.astral.sh/uv/getting-started/installation"
        raise RuntimeError(f"uv not found. Please install it: {url}")
