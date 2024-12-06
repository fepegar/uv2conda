from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Union

import yaml

from .pip import read_requirements_file
from .python import is_valid_python_version
from .uv import get_requirents_from_project_dir

if TYPE_CHECKING:
    from pathlib import Path

TypePipEnv = dict[str, list[str]]
TypeCondaDependency = Union[str, TypePipEnv]
TypeChannels = list[str]
TypeCondaEnv = dict[str, Union[str, TypeChannels, list[TypeCondaDependency]]]


def make_conda_env_from_dependencies(
    name: str,
    python_version: str,
    channels: list[str] | None = None,
    conda_dependencies: list[str] | None = None,
    pip_dependencies: list[str] | None = None,
    out_path: Path | None = None,
    *,
    return_yaml: bool = False,
) -> TypeCondaEnv | str:
    if not is_valid_python_version(python_version):
        msg = f'Invalid Python version: "{python_version}"'
        raise ValueError(msg)
    env_dict: TypeCondaEnv = {
        "name": name,
    }
    if channels:
        env_dict["channels"] = channels
    if conda_dependencies or pip_dependencies:
        env_dict["dependencies"] = [
            f"python={python_version}",
        ]
        if conda_dependencies:
            env_dict["dependencies"].extend(conda_dependencies)
        if pip_dependencies:
            env_dict["dependencies"].append("pip")
            env_dict["dependencies"].append({"pip": pip_dependencies})

    if return_yaml or out_path is not None:
        yaml_string = env_to_str(env_dict)
        if out_path is not None:
            with out_path.open("w") as f:
                f.write(yaml_string)
        return yaml_string

    return env_dict


def env_to_str(env: TypeCondaEnv | str) -> str:
    if isinstance(env, str):
        env_string = env
    else:
        env_string = yaml.dump(env, sort_keys=False, width=1000)
    return env_string


def make_conda_env_from_requirements_file(
    name: str,
    python_version: str,
    requirements_path: Path,
    channels: list[str] | None = None,
    conda_dependencies: list[str] | None = None,
    out_path: Path | None = None,
    *,
    return_yaml: bool = False,
) -> TypeCondaEnv | str:
    return make_conda_env_from_dependencies(
        name,
        python_version,
        channels=channels,
        conda_dependencies=conda_dependencies,
        pip_dependencies=read_requirements_file(requirements_path),
        out_path=out_path,
        return_yaml=return_yaml,
    )


def make_conda_env_from_project_dir(
    project_dir: Path,
    name: str,
    python_version: str,
    channels: list[str] | None = None,
    conda_dependencies: list[str] | None = None,
    out_path: Path | None = None,
    uv_args: list[str] | None = None,
    requirements_path: Path | None = None,
    *,
    return_yaml: bool = False,
) -> TypeCondaEnv | str:
    pip_requirements = get_requirents_from_project_dir(
        project_dir,
        uv_args=uv_args,
        out_requirements_path=requirements_path,
    )
    return make_conda_env_from_dependencies(
        name,
        python_version,
        channels=channels,
        conda_dependencies=conda_dependencies,
        pip_dependencies=pip_requirements,
        out_path=out_path,
        return_yaml=return_yaml,
    )
