# `uv2conda`

[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
![PyPI](https://img.shields.io/pypi/v/uv2conda)

Tiny Python package to create a [`conda`](https://docs.anaconda.com/miniconda/) environment file from a Python project using [`uv`](https://docs.astral.sh/uv/).

Assuming you have installed `uv`:

```shell
uvx uv2conda \
    --project-dir "/path/to/my/project/" \
    --name "my_conda_env_name" \
    --python "3.12.7" \
    --conda-env-file "my_conda_env.yaml" \
    --requirements-file "requirements.txt" \
    --uv-args "--prerelease=allow"
```

Or, in Python:

```python
from uv2conda import CondaEnvironment

environment = CondaEnvironment.from_project_dir(
    project_dir="/path/to/my/project/",
    name="my_conda_env_name",
    python_version="3.12.7",
    uv_args=["--prerelease=allow"],
)
environment.to_pip_requirements_file("requirements.txt")
environment.to_yaml("environment.yaml")
```

Example for this library:

```console
$ uv2conda --python 3.12.7
[23:17:34] WARNING  Environment name not provided. Using project directory name ("uv2conda")
           INFO     Printing the generated conda environment YAML
```

```yaml
name: uv2conda
dependencies:
  - python=3.12.7
  - pip
  - pip:
      - click==8.1.7
      - colorama==0.4.6 ; sys_platform == 'win32'
      - markdown-it-py==3.0.0
      - mdurl==0.1.2
      - packaging==24.2
      - pygments==2.18.0
      - pyyaml==6.0.2
      - rich==13.9.4
      - shellingham==1.5.4
      - typer==0.15.1
      - typing-extensions==4.12.2
```

## Using `uv2conda` with `pre-commit`

To ensure your Conda environment YAML is up-to-date with your `uv.lock`, your `uv` lock file:

```yaml
- repo: https://github.com/fepegar/uv2conda
  rev: v2.0.0
  hooks:
    - id: uv2conda
```

## Related projects

- [`pyproject2conda`](https://pypi.org/project/pyproject2conda/)
