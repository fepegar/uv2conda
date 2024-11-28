# uv2conda

Tiny package to create a conda environment file from a Python project.

```shell
pip install uv2conda
uv2conda \
    --project-dir "/path/to/my/project/" \
    --name "my_conda_env_name" \
    --python "3.12.7" \
    --conda-env-path "my_conda_env.yaml" \
    --uv-args "--prerelease=allow"
```

From Python:

```python
import uv2conda

uv2conda.make_conda_env_from_project_dir(
    "/path/to/my/project/",
    name="my_conda_env_name",
    python_version="3.12.7",
    out_path="environment.yaml",
    uv_args=["--prerelease=allow"],
)
```
