"""
Abstract base class for JSON-configurable types.
"""

from abc import ABC, abstractmethod
from typing import Self

from .typing import JSON

__all__ = ["Config"]


class Config(ABC):
    @classmethod
    @abstractmethod
    def from_config(cls, **kwargs: JSON) -> Self:
        pass

    @abstractmethod
    def get_config(self) -> JSON:
        pass
