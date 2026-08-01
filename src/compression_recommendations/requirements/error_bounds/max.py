"""
Maximum pointwise error-bounding requirements.
"""

from dataclasses import dataclass
from typing import ClassVar, Literal, Self

from typing_extensions import override  # MSPV 3.12

from ...config import _parse_number
from ...typing import JSON
from ..abc import Requirement
from ..kind import RequirementKind

__all__ = [
    "MaxPointwiseAbsoluteErrorBoundRequirement",
    "MaxPointwiseRelativeErrorBoundRequirement",
]


@dataclass(kw_only=True)
class MaxPointwiseAbsoluteErrorBoundRequirement(Requirement):
    kind: ClassVar[RequirementKind] = RequirementKind.max_pointwise_absolute_error_bound
    value: int | float

    @override
    @classmethod
    def from_config(  # type: ignore
        cls,
        *,
        value: int | float,
        kind: Literal[
            "max-pointwise-absolute-error-bound"
        ] = RequirementKind.max_pointwise_absolute_error_bound.value,
    ) -> Self:
        return cls(value=_parse_number(value))

    @override
    def get_config(self) -> JSON:
        return dict(kind=type(self).kind.get_config(), value=self.value)


@dataclass(kw_only=True)
class MaxPointwiseRelativeErrorBoundRequirement(Requirement):
    kind: ClassVar[RequirementKind] = RequirementKind.max_pointwise_relative_error_bound
    value: int | float

    @override
    @classmethod
    def from_config(  # type: ignore
        cls,
        *,
        value: int | float,
        kind: Literal[
            "max-pointwise-relative-error-bound"
        ] = RequirementKind.max_pointwise_relative_error_bound.value,
    ) -> Self:
        return cls(value=_parse_number(value))

    @override
    def get_config(self) -> JSON:
        return dict(kind=type(self).kind.get_config(), value=self.value)
