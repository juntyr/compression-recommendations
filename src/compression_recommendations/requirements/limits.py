"""
Data limit-preserving requirements.
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
    "DataLimitsRequirement",
]


@dataclass(kw_only=True, slots=True)
class DataLimitsRequirement(Requirement):
    kind: ClassVar[RequirementKind] = RequirementKind.data_limits
    minimum: None | int | float = None
    maximum: None | int | float = None

    @override
    @classmethod
    def from_config(  # type: ignore
        cls,
        *,
        minimum: None | int | float = None,
        maximum: None | int | float = None,
        kind: Literal["data-limits"] = RequirementKind.data_limits.value,
    ) -> Self:
        return cls(
            minimum=None if minimum is None else _parse_number(minimum),
            maximum=None if maximum is None else _parse_number(maximum),
        )

    @override
    def get_config(self) -> Mapping[str, JSON]:
        config: dict[str, JSON] = dict(kind=type(self).kind.get_config())
        if self.minimum is not None:
            config["minimum"] = self.minimum
        if self.maximum is not None:
            config["maximum"] = self.maximum
        return config

    @override
    def humanise(self) -> str:
        match (self.minimum, self.maximum):
            case (None, None):
                return "True"
            case (None, maximum):
                return f"x'_i <= {maximum!r} forall i"
            case (minimum, None):
                return f"{minimum!r} <= x'_i forall i"
            case (minimum, maximum):
                return f"{minimum!r} <= x'_i <= {maximum!r} forall i"
