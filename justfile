@install_uv:
	if ! command -v uv >/dev/null 2>&1; then \
		echo "uv is not installed. Installing..."; \
		curl -LsSf https://astral.sh/uv/install.sh | sh; \
	fi

setup: install_uv
    uv sync --all-extras --all-groups
    uv run pre-commit install

bump: setup
    uv run bump-my-version bump patch --verbose
