# uv2conda

Tiny package to create a conda environment file from a Python project.

For now, the easiest way to use `uv2conda` is with [`uvx`](https://docs.astral.sh/uv/guides/tools/), which is installed with [`uv`](https://docs.astral.sh/uv/getting-started/installation/).

```shell
uvx uv2conda \
    --input-project-dir /path/to/your/project_dir \
    --name my_conda_env \
    --python 3.12 \
    --out-conda-path environment.yaml
```

From Python:

```shell
pip install uv2conda
```

And then:

```python
import uv2conda

uv2conda.make_conda_env_from_project_dir(
    "/path/to/your/project_dir",
    name="my_conda_env",
    python_version="3.12",
    out_path="environment.yaml",
    uv_args=["--prerelease=allow"],
)
```
