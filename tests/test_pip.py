from __future__ import annotations

from pathlib import Path

from uv2conda.pip import read_requirements_file


def test_read_requirements_file(tmp_path: Path) -> None:
    requirements_content = """
    # This is a comment
    package_one==1.0.0

    package_two>=2.0.0
    """
    requirements_file = tmp_path / "requirements.txt"
    requirements_file.write_text(requirements_content)

    expected_requirements = ["package_one==1.0.0", "package_two>=2.0.0"]
    assert read_requirements_file(requirements_file) == expected_requirements


def test_read_requirements_file_empty(tmp_path: Path) -> None:
    requirements_file = tmp_path / "requirements.txt"
    requirements_file.write_text("")

    assert read_requirements_file(requirements_file) == []


def test_read_requirements_file_only_comments(tmp_path: Path) -> None:
    requirements_content = """
    # This is a comment
    # Another comment
    """
    requirements_file = tmp_path / "requirements.txt"
    requirements_file.write_text(requirements_content)

    assert read_requirements_file(requirements_file) == []
