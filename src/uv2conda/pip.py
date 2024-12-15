from pathlib import Path


class PipRequirements:
    def __init__(self, requirements: list[str]):
        self._requirements = requirements

    def __str__(self) -> str:
        return "\n".join(self._requirements)

    @classmethod
    def from_requirements_file(cls, requirements_file: Path) -> "PipRequirements":
        with requirements_file.open() as f:
            lines = f.readlines()
        requirements = []
        for line in lines:
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            requirements.append(stripped)
        return cls(requirements)

    def to_requirements_file(self, requirements_file: Path) -> None:
        requirements_file.write_text(str(self))

    def to_list(self) -> list[str]:
        return self._requirements
