import sys
from pathlib import Path

import typer
from loguru import logger
from rich.console import Console
from rich.syntax import Syntax
from typing_extensions import Annotated

from .conda import make_conda_env_from_project_dir

app = typer.Typer()
logger.remove()
logger.add(
    sys.stderr,
    format="<level>{level}</level> | <cyan>{message}</cyan>",
)

@app.command()
def uv2conda(
    project_dir: Annotated[Path, typer.Option(
        "--project-dir",
        "-d",
        file_okay=False,
        dir_okay=True,
        exists=True,
        readable=True,
        help="Path to the input project directory. Defaults to the current directory.",
    )] = Path.cwd().resolve(),
    name: Annotated[str, typer.Option(
        "--name",
        "-n",
        help="Name of the conda environment. Defaults to the project directory name.",
    )] = "",
    python_version: Annotated[str, typer.Option(
        "--python",
        "-p",
        help="Python version. Defaults to the pinned version in the project directory.",
    )] = "",
    conda_env_path: Annotated[Path, typer.Option(
        "--conda-env-path",
        "-c",
        file_okay=True,
        dir_okay=False,
        writable=True,
        help="Path to the output conda environment file.",
    )] = Path("environment.yaml"),
    show: Annotated[bool, typer.Option(
        "--show",
        "-s",
        help="Print the contents of the generated conda environment file.",
    )] = False,
    uv_args: Annotated[list[str], typer.Option(
        "--uv-args",
        "-u",
        help="Extra arguments to pass to uv export. May be used multiple times.",
    )] = [],
):
    if not name:
        name = project_dir.name
        msg = f'Environment name not provided. Using project directory name ("{name}")'
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
            raise typer.Abort()

    if uv_args:
        raw_args = uv_args[:]
        uv_args = []
        for arg in raw_args:
            uv_args.extend(arg.split())
        logger.info(f"Extra args for uv: {uv_args}")

    make_conda_env_from_project_dir(
        project_dir,
        name=name,
        python_version=python_version,
        out_path=conda_env_path,
        uv_args=uv_args,
    )
    logger.success(f'Conda environment file created at "{conda_env_path}"')

    if show:
        console = Console()
        syntax = Syntax.from_path(str(conda_env_path))
        console.print(syntax)
