from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Literal

import yaml

from .console import print_syntax
from .pip import PipRequirements
from .python import check_python_version
from .python import get_python_version_from_project_dir
from .uv import get_pip_requirements_from_project_dir

if TYPE_CHECKING:
    from pathlib import Path

TypePipEnv = dict[Literal["pip"], list[str]]
TypeCondaDependency = str | TypePipEnv
TypeChannels = list[str]
TypeCondaEnvKey = Literal["name", "channels", "dependencies"]
TypeCondaEnvDict = dict[TypeCondaEnvKey, str | TypeChannels | list[TypeCondaDependency]]


class CondaEnvironment:
    def __init__(
        self,
        name: str,
        python_version: str,
        channels: list[str] | None = None,
        conda_dependencies: list[str] | None = None,
        pip_requirements: list[str] | None = None,
    ):
        self._name = name
        check_python_version(python_version)
        self._python_version = python_version
        self._channels = channels
        self._conda_dependencies = conda_dependencies
        if pip_requirements is None:
            self._pip_requirements = None
        else:
            self._pip_requirements = PipRequirements(pip_requirements)

    @classmethod
    def from_project_dir(
        cls,
        project_dir: Path | None = None,
        name: str | None = None,
        python_version: str | None = None,
        channels: list[str] | None = None,
        conda_dependencies: list[str] | None = None,
        uv_args: list[str] | None = None,
        requirements_path: Path | None = None,
    ) -> CondaEnvironment:
        if project_dir is None:
            project_dir = Path.cwd()

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

        pip_requirements = get_pip_requirements_from_project_dir(
            project_dir,
            uv_args=uv_args,
            out_requirements_path=requirements_path,
        )

        return cls(
            name,
            python_version,
            channels=channels,
            conda_dependencies=conda_dependencies,
            pip_requirements=pip_requirements.to_list(),
        )

    @classmethod
    def from_pip_requirements_file(
        cls,
        python_version: str,
        pip_requirements_path: Path,
        name: str | None = None,
        channels: list[str] | None = None,
    ) -> CondaEnvironment:
        pip_requirements = PipRequirements.from_requirements_file(pip_requirements_path)
        if name is None:
            name = pip_requirements_path.parent.name
        return cls(
            name,
            python_version,
            channels=channels,
            pip_requirements=pip_requirements.to_list(),
        )

    def print(self):
        print_syntax(str(self))

    def __str__(self) -> str:
        return self.to_yaml()

    def to_yaml(self, out_path: Path | None = None) -> str:
        string = yaml.dump(
            self.to_dict(),
            sort_keys=False,
            width=1000,
            Dumper=_IndentDumper,
        )
        if out_path is not None:
            with out_path.open("w") as f:
                f.write(string)
        return string

    def to_dict(self) -> TypeCondaEnvDict:
        env_dict: TypeCondaEnvDict = {
            "name": self._name,
        }
        if self._channels:
            env_dict["channels"] = self._channels
        if self._conda_dependencies or self._pip_requirements:
            dependencies_list: list[TypeCondaDependency] = [
                f"python={self._python_version}",
            ]
            if self._conda_dependencies:
                dependencies_list.extend(self._conda_dependencies)
            if self._pip_requirements is not None:
                dependencies_list.append("pip")
                dependencies_list.append({"pip": self._pip_requirements.to_list()})

            env_dict["dependencies"] = dependencies_list

        return env_dict

    def to_pip_requirements_file(self, out_path: Path) -> None:
        if self._pip_requirements is None:
            msg = "No pip requirements found in the environment"
            raise ValueError(msg)
        self._pip_requirements.to_requirements_file(out_path)


# Adapted from https://reorx.com/blog/python-yaml-tips/
class _IndentDumper(yaml.Dumper):
    def increase_indent(self, flow: bool = False, indentless: bool = False) -> None:
        return super().increase_indent(flow=flow, indentless=False)
