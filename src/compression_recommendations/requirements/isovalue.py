"""
Isovalue-preserving requirements.
"""

from collections.abc import Mapping
from dataclasses import dataclass
from typing import ClassVar, Literal, Self

from typing_extensions import override  # MSPV 3.12

from ..config import _parse_number
from ..typing import JSON
from .abc import Requirement
from .kind import RequirementKind

__all__ = [
    "IsovalueRequirement",
]


@dataclass(kw_only=True, slots=True)
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
    def get_config(self) -> Mapping[str, JSON]:
        return dict(kind=type(self).kind.get_config(), value=self.value)

    @override
    def humanise(self) -> str:
        return f"(x_i ⋛ {self.value!r}) == (x'_i ⋛ {self.value!r}) forall i"
