import importlib.metadata

from .conda import CondaEnvironment

__version__ = importlib.metadata.version(__name__)

__all__ = [
    "CondaEnvironment",
]
