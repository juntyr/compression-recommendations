"""
Mean error-bounding requirements.
"""

from collections.abc import Mapping
from dataclasses import dataclass
from typing import ClassVar, Literal, Self

from typing_extensions import override  # MSPV 3.12

from ...config import _parse_number
from ...typing import JSON
from ..abc import Requirement
from ..kind import RequirementKind

__all__ = [
    "MeanAbsoluteErrorBoundRequirement",
    "MeanRelativeErrorBoundRequirement",
]


@dataclass(kw_only=True, slots=True)
class MeanAbsoluteErrorBoundRequirement(Requirement):
    kind: ClassVar[RequirementKind] = RequirementKind.mean_absolute_error_bound
    value: int | float

    @override
    @classmethod
    def from_config(  # type: ignore
        cls,
        *,
        value: int | float,
        kind: Literal[
            "mean-absolute-error-bound"
        ] = RequirementKind.mean_absolute_error_bound.value,
    ) -> Self:
        return cls(value=_parse_number(value))

    @override
    def get_config(self) -> Mapping[str, JSON]:
        return dict(kind=type(self).kind.get_config(), value=self.value)


@dataclass(kw_only=True, slots=True)
class MeanRelativeErrorBoundRequirement(Requirement):
    kind: ClassVar[RequirementKind] = RequirementKind.mean_relative_error_bound
    value: int | float

    @override
    @classmethod
    def from_config(  # type: ignore
        cls,
        *,
        value: int | float,
        kind: Literal[
            "mean-relative-error-bound"
        ] = RequirementKind.mean_relative_error_bound.value,
    ) -> Self:
        return cls(value=_parse_number(value))

    @override
    def get_config(self) -> Mapping[str, JSON]:
        return dict(kind=type(self).kind.get_config(), value=self.value)
