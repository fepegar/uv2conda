from pathlib import Path

import typer

from .conda import make_conda_env_from_project_dir

app = typer.Typer()


@app.command(
    no_args_is_help=True,
    context_settings={
        "allow_extra_args": True,
        "ignore_unknown_options": True,
    },
)
def uv2conda(
    input_project_dir: Path = typer.Option(
        ...,
        "--input-project-dir",
        "-i",
        file_okay=False,
        dir_okay=True,
        exists=True,
        readable=True,
        help="Path to the project directory",
    ),
    name: str = typer.Option(
        ...,
        "--name",
        "-n",
        help="Name of the conda environment",
    ),
    python_version: str = typer.Option(
        ...,
        "--python",
        "-p",
        help="Python version",
    ),
    out_conda_path = typer.Option(
        ...,
        "--out-conda-path",
        "-o",
        file_okay=True,
        dir_okay=False,
        writable=True,
        help="Path to the output conda environment file",
    ),
    context: typer.Context = typer.Option(None),
):
    make_conda_env_from_project_dir(
        input_project_dir,
        name=name,
        python_version=python_version,
        out_path=out_conda_path,
        uv_args=context.args,
    )
