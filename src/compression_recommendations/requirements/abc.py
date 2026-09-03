"""
Abstract base class for requirements.
"""

from abc import ABC
from typing import ClassVar, Self

from typing_extensions import override  # MSPV 3.12

from ..config import Config
from ..typing import JSON
from .kind import RequirementKind

__all__ = ["Requirement"]


class Requirement(Config, ABC):
    __slots__: tuple[str, ...] = ()

    kind: ClassVar[RequirementKind]

    @override
    @classmethod
    def from_config(cls, *, kind: str, **kwargs: JSON) -> Self:  # type: ignore
        return RequirementKind.from_config(kind).cls.from_config(
            **kwargs  # type: ignore
        )
