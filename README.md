# uv2conda

Tiny package to create a conda environment file from a Python project.

For now, the easiest way to use `uv2conda` is with [`uvx`](https://docs.astral.sh/uv/guides/tools/), which is installed with [`uv`](https://docs.astral.sh/uv/getting-started/installation/).

```bash
uvx --from git+https://github.com/fepegar/uv2conda \
    uv2conda \
        --input-project-dir /path/to/your/project \
        --name my_conda_env \
        --python 3.12 \
        --out-conda-path environment.yaml
```
