import sys
from pathlib import Path
from typing import Annotated
from typing import Optional

import typer
from loguru import logger

from . import __version__
from .conda import CondaEnvironment

app = typer.Typer(
    pretty_exceptions_show_locals=False,
)
logger.remove()
logger.add(
    sys.stderr,
    format="{level:<8} | <level>{message}</level>",
)
current_dir = Path.cwd().resolve()
default_uv_args: list[str] = []
default_conda_channels: list[str] = []


def _version_callback(value: bool) -> None:
    if value:
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
                " in the project directory (in the `.python-version` file)."
            ),
        ),
    ] = "",
    conda_env_path: Annotated[
        Optional[Path],
        typer.Option(
            "--conda-env-file",
            "-f",
            file_okay=True,
            dir_okay=False,
            writable=True,
            help=(
                "Path to the output conda environment file."
                " For example: `-f environment.yaml`"
            ),
            rich_help_panel="Output files",
        ),
    ] = None,
    requirements_path: Annotated[
        Optional[Path],
        typer.Option(
            "--requirements-file",
            "-r",
            file_okay=True,
            dir_okay=False,
            writable=True,
            help=(
                "Path to the output requirements file."
                " For example: `-r requirements.txt`"
            ),
            rich_help_panel="Output files",
        ),
    ] = None,
    channels: Annotated[
        list[str],
        typer.Option(
            "--channel",
            "-c",
            help=(
                "Conda channel to add. May be used multiple times. For example:"
                " `-c conda-forge -c nvidia`"
            ),
        ),
    ] = default_conda_channels,
    show: Annotated[
        bool,
        typer.Option(
            help="Print the contents of the generated conda environment file.",
        ),
    ] = True,
    uv_args: Annotated[
        list[str],
        typer.Option(
            "--uv-arg",
            "-u",
            help=(
                "Extra argument to pass to `uv export`. May be used multiple times."
                " For example: `-u --no-emit-workspace -u --prerelease=allow`. For more"
                " options, see `uv export --help`."
            ),
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
            help="Show the version and exit.",
        ),
    ] = None,
) -> None:
    """Create a conda environment and/or PIP requirements file from a package."""

    if not show and conda_env_path is None and requirements_path is None:
        logger.error(
            "At least one of --conda-env-file, --requirements-file, or --show"
            " must be provided.",
        )
        raise typer.Abort

    output_conda_env = show or conda_env_path is not None
    if not name:
        name = project_dir.name
        if output_conda_env:
            msg = (
                "Environment name not provided."
                f' Using project directory name ("{name}")'
            )
            logger.warning(msg)

    if not python_version:
        pinned_python_version_filepath = project_dir / ".python-version"
        if pinned_python_version_filepath.exists():
            python_version = pinned_python_version_filepath.read_text().strip()
            msg = (
                "Python version not provided. Using pinned version"
                f' found in "{pinned_python_version_filepath}" ("{python_version}")'
            )
            logger.warning(msg)
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

    environment = CondaEnvironment.from_project_dir(
        project_dir,
        name=name,
        python_version=python_version,
        channels=channels,
        uv_args=uv_args,
    )

    _check_overwrite(conda_env_path, requirements_path, force=force)
    if conda_env_path is not None:
        environment.to_yaml(out_path=conda_env_path)
        logger.success(f'Conda environment file created at "{conda_env_path}"')
    if requirements_path is not None:
        environment.to_pip_requirements_file(out_path=requirements_path)
        logger.success(f'Requirements file created at "{requirements_path}"')

    if show:
        logger.info("Printing contents of the generated conda environment file")
        environment.print()


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
