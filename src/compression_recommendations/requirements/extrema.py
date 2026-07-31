"""
Extrema-preserving requirements.
"""

from dataclasses import dataclass
from typing import ClassVar, Literal, Self

from typing_extensions import override  # MSPV 3.12

from ..typing import JSON, _parse_number
from .abc import Requirement
from .kind import RequirementKind

__all__ = [
    "GlobalMinimumRequirement",
    "GlobalMaximumRequirement",
]


@dataclass(kw_only=True)
class GlobalMinimumRequirement(Requirement):
    kind: ClassVar[RequirementKind] = RequirementKind.global_minimum
    value: int | float

    @override
    @classmethod
    def from_config(  # type: ignore
        cls,
        *,
        value: int | float,
        kind: Literal["global-minimum"] = RequirementKind.global_minimum.value,
    ) -> Self:
        return cls(value=_parse_number(value))

    @override
    def get_config(self) -> JSON:
        return dict(kind=type(self).kind.get_config(), value=self.value)


@dataclass(kw_only=True)
class GlobalMaximumRequirement(Requirement):
    kind: ClassVar[RequirementKind] = RequirementKind.global_maximum
    value: int | float

    @override
    @classmethod
    def from_config(  # type: ignore
        cls,
        *,
        value: int | float,
        kind: Literal["global-maximum"] = RequirementKind.global_maximum.value,
    ) -> Self:
        return cls(value=_parse_number(value))

    @override
    def get_config(self) -> JSON:
        return dict(kind=type(self).kind.get_config(), value=self.value)
