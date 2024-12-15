from __future__ import annotations

from pathlib import Path

from uv2conda.pip import PipRequirements


def test_read_requirements_file(tmp_path: Path) -> None:
    requirements_content = """
    # This is a comment
    package_one==1.0.0
    # Another comment
    package_two>=2.0.0
    """
    requirements_file = tmp_path / "requirements.txt"
    requirements_file.write_text(requirements_content)

    expected_requirements = ["package_one==1.0.0", "package_two>=2.0.0"]
    read_requirements = PipRequirements.from_requirements_file(requirements_file)
    assert read_requirements.to_list() == expected_requirements


def test_read_requirements_file_empty(tmp_path: Path) -> None:
    requirements_file = tmp_path / "requirements.txt"
    requirements_file.write_text("")

    read_requirements = PipRequirements.from_requirements_file(requirements_file)
    assert read_requirements.to_list() == []


def test_read_requirements_file_only_comments(tmp_path: Path) -> None:
    requirements_content = """
    # This is a comment
    # Another comment
    """
    requirements_file = tmp_path / "requirements.txt"
    requirements_file.write_text(requirements_content)

    read_requirements = PipRequirements.from_requirements_file(requirements_file)
    assert read_requirements.to_list() == []
