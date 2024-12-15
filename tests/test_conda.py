import pytest
import yaml

from uv2conda.conda import CondaEnvironment


def test_conda_environment_init():
    env = CondaEnvironment(
        name="test_env",
        python_version="3.9.1",
        channels=["conda-forge"],
        conda_dependencies=["numpy", "pandas"],
        pip_requirements=["requests==2.31.0"],
    )
    assert env._name == "test_env"
    assert env._python_version == "3.9.1"
    assert env._channels == ["conda-forge"]
    assert env._conda_dependencies == ["numpy", "pandas"]
    assert env._pip_requirements is not None
    assert env._pip_requirements.to_list() == ["requests==2.31.0"]


def test_conda_environment_invalid_python():
    with pytest.raises(ValueError):
        CondaEnvironment(
            name="test_env",
            python_version="invalid",
        )


def test_conda_environment_to_dict():
    env = CondaEnvironment(
        name="test_env",
        python_version="3.9.1",
        channels=["conda-forge"],
        conda_dependencies=["numpy", "pandas"],
        pip_requirements=["requests==2.31.0"],
    )
    env_dict = env.to_dict()
    assert env_dict["name"] == "test_env"
    assert env_dict["channels"] == ["conda-forge"]
    assert "python=3.9.1" in env_dict["dependencies"]
    assert "numpy" in env_dict["dependencies"]
    assert "pandas" in env_dict["dependencies"]
    assert "pip" in env_dict["dependencies"]
    pip_deps = next(d for d in env_dict["dependencies"] if isinstance(d, dict))
    assert pip_deps["pip"] == ["requests==2.31.0"]


def test_conda_environment_to_yaml(tmp_path):
    env = CondaEnvironment(
        name="test_env",
        python_version="3.9.1",
        channels=["conda-forge"],
        conda_dependencies=["numpy", "pandas"],
        pip_requirements=["requests==2.31.0"],
    )

    # Test yaml string output
    yaml_str = env.to_yaml()
    parsed = yaml.safe_load(yaml_str)
    assert parsed["name"] == "test_env"

    # Test file output
    out_file = tmp_path / "environment.yml"
    env.to_yaml(out_file)
    assert out_file.exists()
    with out_file.open() as f:
        parsed = yaml.safe_load(f)
    assert parsed["name"] == "test_env"


def test_conda_environment_from_pip_requirements(tmp_path):
    requirements_file = tmp_path / "requirements.txt"
    requirements_file.write_text("requests==2.31.0\npandas==2.0.0")

    env = CondaEnvironment.from_pip_requirements_file(
        python_version="3.9.1",
        pip_requirements_path=requirements_file,
        name="test_env",
        channels=["conda-forge"],
    )

    assert env._name == "test_env"
    assert env._python_version == "3.9.1"
    assert env._channels == ["conda-forge"]
    assert env._pip_requirements is not None
    assert "requests==2.31.0" in env._pip_requirements.to_list()
    assert "pandas==2.0.0" in env._pip_requirements.to_list()


def test_conda_environment_to_pip_requirements(tmp_path):
    env = CondaEnvironment(
        name="test_env",
        python_version="3.9.1",
        pip_requirements=["requests==2.31.0"],
    )

    out_file = tmp_path / "requirements.txt"
    env.to_pip_requirements_file(out_file)
    assert out_file.exists()
    assert out_file.read_text().strip() == "requests==2.31.0"


def test_conda_environment_no_pip_requirements():
    env = CondaEnvironment(
        name="test_env",
        python_version="3.9.1",
    )

    with pytest.raises(ValueError, match="No pip requirements found"):
        env.to_pip_requirements_file("requirements.txt")
