from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path

import typer

from .logger import logger
from .pip import PipRequirements


def write_requirements_file_from_project_dir(
    project_dir: Path,
    out_path: Path,
    extra_args: list[str] | None = None,
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

    try:
        subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError as e:
        command_str = " ".join(command)
        msg = (
            "Error creating requirements file from uv project."
            f"\nCommand: {command_str}"
            f"\nOutput from uv: {e.stderr.strip()}"
        )
        logger.error(msg)
        raise typer.Exit(1) from e


def get_pip_requirements_from_project_dir(
    project_dir: Path,
    uv_args: list[str] | None = None,
    out_requirements_path: Path | None = None,
) -> PipRequirements:
    logger.error("test")
    if out_requirements_path is None:
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete_on_close=False
        ) as f:
            requirements_path = Path(f.name)
        write_requirements_file_from_project_dir(
            project_dir,
            requirements_path,
            extra_args=uv_args,
        )
        requirements = PipRequirements.from_requirements_file(requirements_path)

    else:
        write_requirements_file_from_project_dir(
            project_dir,
            out_requirements_path,
            extra_args=uv_args,
        )
        requirements = PipRequirements.from_requirements_file(out_requirements_path)
    return requirements


def _check_uv_installed() -> None:
    if shutil.which("uv") is None:
        url = "https://docs.astral.sh/uv/getting-started/installation"
        msg = f"uv not found. Please install it: {url}"
        raise RuntimeError(msg)
