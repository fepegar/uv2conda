from __future__ import annotations

from typing import TYPE_CHECKING

import yaml

from .pip import read_requirements_file
from .python import get_python_version_from_project_dir
from .python import is_valid_python_version
from .uv import get_requirents_from_project_dir

if TYPE_CHECKING:
    from pathlib import Path

TypePipEnv = dict[str, list[str]]
TypeCondaDependency = str | TypePipEnv
TypeChannels = list[str]
TypeCondaEnv = dict[str, str | TypeChannels | list[TypeCondaDependency]]


def make_conda_env_from_dependencies(
    name: str,
    python_version: str,
    channels: list[str] | None = None,
    conda_dependencies: list[str] | None = None,
    pip_dependencies: list[str] | None = None,
    out_path: Path | None = None,
) -> TypeCondaEnv:
    if not is_valid_python_version(python_version):
        msg = f'Invalid Python version: "{python_version}"'
        raise ValueError(msg)
    env_dict: TypeCondaEnv = {
        "name": name,
    }
    if channels:
        env_dict["channels"] = channels
    if conda_dependencies or pip_dependencies:
        dependencies_list: list[TypeCondaDependency] = [
            f"python={python_version}",
        ]
        if conda_dependencies:
            dependencies_list.extend(conda_dependencies)
        if pip_dependencies:
            dependencies_list.append("pip")
            dependencies_list.append({"pip": pip_dependencies})

        env_dict["dependencies"] = dependencies_list

    if out_path is not None:
        env_to_file(env_dict, out_path)

    return env_dict


def env_to_str(env: TypeCondaEnv | str) -> str:
    if isinstance(env, str):
        env_string = env
    else:
        env_string = yaml.dump(env, sort_keys=False, width=1000)
    return env_string


def env_to_file(env: TypeCondaEnv, out_path: Path) -> None:
    with out_path.open("w") as f:
        f.write(env_to_str(env))


def make_conda_env_from_requirements_file(
    name: str,
    python_version: str,
    requirements_path: Path,
    channels: list[str] | None = None,
    conda_dependencies: list[str] | None = None,
    out_path: Path | None = None,
) -> TypeCondaEnv | str:
    return make_conda_env_from_dependencies(
        name,
        python_version,
        channels=channels,
        conda_dependencies=conda_dependencies,
        pip_dependencies=read_requirements_file(requirements_path),
        out_path=out_path,
    )


def make_conda_env_from_project_dir(
    project_dir: Path,
    name: str | None = None,
    python_version: str | None = None,
    channels: list[str] | None = None,
    conda_dependencies: list[str] | None = None,
    out_path: Path | None = None,
    uv_args: list[str] | None = None,
    requirements_path: Path | None = None,
) -> TypeCondaEnv | str:
    pip_requirements = get_requirents_from_project_dir(
        project_dir,
        uv_args=uv_args,
        out_requirements_path=requirements_path,
    )
    if name is None:
        name = project_dir.name
    if python_version is None:
        python_version = get_python_version_from_project_dir(project_dir)
        if python_version is None:
            msg = (
                "A Python version must be specified either via the "
                "--python-version option or by creating a "
                ".python-version file in the project directory."
            )
            raise ValueError(msg)
    return make_conda_env_from_dependencies(
        name,
        python_version,
        channels=channels,
        conda_dependencies=conda_dependencies,
        pip_dependencies=pip_requirements,
        out_path=out_path,
    )
