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
    env: TypeCondaEnv = {
        "name": name,
    }
    if channels is not None:
        env["channels"] = channels
    if conda_dependencies is not None or pip_dependencies is not None:
        env["dependencies"] = [
            f"python={python_version}",
        ]
        if conda_dependencies:
            env["dependencies"].extend(conda_dependencies)
        if pip_dependencies:
            env["dependencies"].append("pip")
            env["dependencies"].append({"pip": pip_dependencies})

    if return_yaml or out_path is not None:
        yaml_string = env_to_str(env)
        if out_path is not None:
            with out_path.open("w") as f:
                f.write(yaml_string)
        return yaml_string

    return env


def env_to_str(env: TypeCondaEnv | str) -> str:
    if isinstance(env, str):
        env_string = env
    else:
        env_string = yaml.dump(env, sort_keys=False, width=1000)
    return env_string


def make_conda_env_from_requirements_file(
    requirements_path: Path,
    *args,
    **kwargs,
) -> TypeCondaEnv | str:
    return make_conda_env_from_dependencies(
        *args,
        **kwargs,
        pip_dependencies=read_requirements_file(requirements_path),
    )


def make_conda_env_from_project_dir(
    project_dir: Path,
    *args,
    **kwargs,
) -> TypeCondaEnv | str:
    pip_requirements = get_requirents_from_project_dir(
        project_dir,
        uv_args=kwargs.pop("uv_args", None),
        out_requirements_path=kwargs.pop("requirements_path", None),
    )
    return make_conda_env_from_dependencies(
        *args,
        **kwargs,
        pip_dependencies=pip_requirements,
    )
