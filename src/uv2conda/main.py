from pathlib import Path
from typing import Annotated
from typing import Optional

import typer

from . import __version__
from .conda import CondaEnvironment
from .logger import logger

app = typer.Typer(
    pretty_exceptions_show_locals=False,
)
current_dir = Path.cwd().resolve()
default_uv_args: list[str] = []
default_conda_channels: list[str] = []


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(__version__)
        raise typer.Exit


@app.command(context_settings={"allow_extra_args": True})
def uv2conda(
    ctx: typer.Context,
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
                " `-c conda-forge -c nvidia`."
            ),
        ),
    ] = default_conda_channels,
    quiet: Annotated[
        bool,
        typer.Option(
            "--quiet",
            "-q",
            help="Do not print the contents of the generated conda environment file.",
        ),
    ] = False,
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
    verbose: Annotated[
        bool,
        typer.Option(
            "--verbose",
            "-v",
            help="Print verbose output.",
        ),
    ] = False,
) -> None:
    """Create a Conda environment or requirements file from a project directory.

    Extra arguments for `uv export` can be passed using `--` followed by the
    arguments. For example: `uv2conda -- --no-emit-workspace --prerelease=allow`.

    For more information about `uv export`, see `uv export --help` or `uv help export`.
    """
    must_print_env = not quiet
    must_write_conda_env = conda_env_path is not None
    must_create_yaml = must_print_env or must_write_conda_env

    if quiet and not must_write_conda_env and requirements_path is None:
        logger.error(
            "If --quiet is used, at least one of --conda-env-file or"
            "--requirements-file must be provided."
        )
        raise typer.Abort

    if not name:
        name = project_dir.name
        if must_create_yaml and verbose:
            msg = (
                "Environment name not provided."
                f' Using project directory name ("{name}")'
            )
            logger.warning(msg)

    if not python_version:
        pinned_python_version_filepath = project_dir / ".python-version"
        if pinned_python_version_filepath.exists():
            python_version = pinned_python_version_filepath.read_text().strip()
            if verbose:
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

    if ctx.args and verbose:
        logger.info(f"Extra arguments for `uv export`: {ctx.args}")

    environment = CondaEnvironment.from_project_dir(
        project_dir,
        name=name,
        python_version=python_version,
        channels=channels,
        uv_args=ctx.args,
    )

    _check_overwrite(conda_env_path, requirements_path, force=force)
    if conda_env_path is not None:
        environment.to_yaml(out_path=conda_env_path)
        if verbose:
            logger.info(f'Conda environment file created at "{conda_env_path}"')
    if requirements_path is not None:
        environment.to_pip_requirements_file(out_path=requirements_path)
        if verbose:
            logger.info(f'Requirements file created at "{requirements_path}"')

    if not quiet:
        if verbose:
            logger.info("Printing the generated conda environment YAML")
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
    typer.confirm(msg, abort=True, err=True)
