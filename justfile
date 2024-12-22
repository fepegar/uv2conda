default:
    @just --list

@install_uv:
	if ! command -v uv >/dev/null 2>&1; then \
		echo "uv is not installed. Installing..."; \
		curl -LsSf https://astral.sh/uv/install.sh | sh; \
	fi

setup: install_uv
    uv sync --all-extras --all-groups
    uv run -- pre-commit install --install-hooks

bump part='patch': install_uv
    uv run bump-my-version bump {{part}} --verbose

release: install_uv
    rm -rf dist
    uv build
    uv publish -t $UV_PUBLISH_TOKEN

changelog: install_uv
    uvx git-changelog --output CHANGELOG.md

ruff: install_uv
    uvx ruff check
    uvx ruff format

test: install_uv
    uv run pytest

push:
    git push
    git push --tags
