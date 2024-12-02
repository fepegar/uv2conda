@install_uv:
	if ! command -v uv >/dev/null 2>&1; then \
		echo "uv is not installed. Installing..."; \
		curl -LsSf https://astral.sh/uv/install.sh | sh; \
	fi

setup: install_uv
    uv sync --all-extras --all-groups
    uv run pre-commit install

bump: install_uv
    uv run bump-my-version bump patch --verbose

release: install_uv
    rm -rf dist
    uv build
    uv publish -t $UV_PUBLISH_TOKEN
