"""
Lossless compression requirement.
"""

from collections.abc import Mapping
from dataclasses import dataclass
from typing import ClassVar, Literal, Self

from typing_extensions import override  # MSPV 3.12

from ..typing import JSON
from .abc import Requirement
from .kind import RequirementKind

__all__ = ["LosslessRequirement"]


@dataclass(kw_only=True, slots=True)
class LosslessRequirement(Requirement):
    kind: ClassVar[RequirementKind] = RequirementKind.lossless

    @override
    @classmethod
    def from_config(  # type: ignore
        cls,
        *,
        kind: Literal["lossless"] = RequirementKind.lossless.value,
    ) -> Self:
        return cls()

    @override
    def get_config(self) -> Mapping[str, JSON]:
        return dict(kind=type(self).kind.get_config())
