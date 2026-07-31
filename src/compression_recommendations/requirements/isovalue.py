"""
Isovalue-preserving requirements.
"""

from dataclasses import dataclass
from typing import ClassVar, Literal, Self

from typing_extensions import override  # MSPV 3.12

from ..typing import JSON, _parse_number
from .abc import Requirement
from .kind import RequirementKind

__all__ = [
    "IsovalueRequirement",
]


@dataclass(kw_only=True)
class IsovalueRequirement(Requirement):
    kind: ClassVar[RequirementKind] = RequirementKind.isovalue
    value: int | float

    @override
    @classmethod
    def from_config(  # type: ignore
        cls,
        *,
        value: int | float,
        kind: Literal["isovalue"] = RequirementKind.isovalue.value,
    ) -> Self:
        return cls(value=_parse_number(value))

    @override
    def get_config(self) -> JSON:
        return dict(kind=type(self).kind.get_config(), value=self.value)
