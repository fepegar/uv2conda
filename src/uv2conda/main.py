import sys
from pathlib import Path
from typing import Annotated
from typing import Optional

import typer
from loguru import logger
from rich.console import Console
from rich.syntax import Syntax

from . import __version__
from .conda import env_to_str
from .conda import make_conda_env_from_project_dir

app = typer.Typer()
logger.remove()
logger.add(
    sys.stderr,
    format="<level>{level}</level> | <cyan>{message}</cyan>",
)
current_dir = Path.cwd().resolve()
default_uv_args = []


def _version_callback() -> None:
    typer.echo(__version__)
    raise typer.Exit


@app.command()
def uv2conda(
    project_dir: Annotated[
        Path,
        typer.Option(
            "--project-dir",
            "-d",
            file_okay=False,
            dir_okay=True,
            exists=True,
            readable=True,
            help=(
                "Path to the input project directory."
                " Defaults to the current directory."
            ),
        ),
    ] = current_dir,
    name: Annotated[
        str,
        typer.Option(
            "--name",
            "-n",
            help=(
                "Name of the conda environment."
                " Defaults to the project directory name."
            ),
        ),
    ] = "",
    python_version: Annotated[
        str,
        typer.Option(
            "--python",
            "-p",
            help=(
                "Python version. Defaults to the pinned version"
                " in the project directory."
            ),
        ),
    ] = "",
    conda_env_path: Annotated[
        Optional[Path],
        typer.Option(
            "--conda-env-path",
            "-c",
            file_okay=True,
            dir_okay=False,
            writable=True,
            help="Path to the output conda environment file.",
        ),
    ] = None,
    requirements_path: Annotated[
        Optional[Path],
        typer.Option(
            "--requirements-path",
            "-r",
            file_okay=True,
            dir_okay=False,
            writable=True,
            help="Path to the output requirements file.",
        ),
    ] = None,
    show: Annotated[
        bool,
        typer.Option(
            help="Print the contents of the generated conda environment file.",
        ),
    ] = True,
    uv_args: Annotated[
        list[str],
        typer.Option(
            "--uv-args",
            "-u",
            help="Extra arguments to pass to `uv export`. May be used multiple times.",
        ),
    ] = default_uv_args,
    force: Annotated[
        bool,
        typer.Option(
            "--yes",
            "-y",
            help="Overwrite the output files if they already exist.",
        ),
    ] = False,
    version: Annotated[
        Optional[bool],
        typer.Option(
            "--version",
            callback=_version_callback,
            is_eager=True,
        ),
    ] = None,
) -> None:
    if not name:
        name = project_dir.name
        msg = f'Environment name not provided. Using project directory name ("{name}")'
        logger.info(msg)

    if not python_version:
        pinned_python_version_filepath = project_dir / ".python-version"
        if pinned_python_version_filepath.exists():
            python_version = pinned_python_version_filepath.read_text().strip()
            msg = (
                "Python version not provided. Using pinned version"
                f' found in "{pinned_python_version_filepath}" ("{python_version}")'
            )
            logger.info(msg)
        else:
            msg = (
                "A Python version must be provided if there is no pinned version in"
                f' the project directory ("{pinned_python_version_filepath}")'
            )
            logger.error(msg)
            raise typer.Abort

    if uv_args:
        raw_args = uv_args[:]
        uv_args = []
        for arg in raw_args:
            uv_args.extend(arg.split())
        logger.info(f"Extra args for uv: {uv_args}")

    _check_overwrite(conda_env_path, requirements_path, force=force)

    env = make_conda_env_from_project_dir(
        project_dir,
        name=name,
        python_version=python_version,
        out_path=conda_env_path,
        uv_args=uv_args,
        requirements_path=requirements_path,
    )
    if conda_env_path is not None:
        logger.success(f'Conda environment file created at "{conda_env_path}"')
    if requirements_path is not None:
        logger.success(f'Requirements file created at "{requirements_path}"')

    if show:
        logger.info("Printing contents of the generated conda environment file")
        console = Console()
        env_yaml = env_to_str(env)
        syntax = Syntax(env_yaml, "yaml", background_color="default")
        console.print(syntax)


def _check_overwrite(
    conda_env_path: Optional[Path],
    requirements_path: Optional[Path],
    *,
    force: bool,
) -> None:
    if conda_env_path is not None and conda_env_path.exists() and not force:
        _ask("Conda environment file", conda_env_path)
    if requirements_path is not None and requirements_path.exists() and not force:
        _ask("Requirements file", requirements_path)


def _ask(prefix: str, path: Path) -> None:
    msg = f'{prefix} "{path}" already exists. Would you like to overwrite it?'
    typer.confirm(msg, abort=True)
