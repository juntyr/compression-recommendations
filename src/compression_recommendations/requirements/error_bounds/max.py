"""
Maximum pointwise error-bounding requirements.
"""

from collections.abc import Mapping
from dataclasses import dataclass
from typing import ClassVar, Literal, Self

from typing_extensions import override  # MSPV 3.12

from ...config import _parse_number, _to_camel_case
from ...typing import JSON
from ..abc import Requirement
from ..kind import RequirementKind

__all__ = [
    "MaxPointwiseAbsoluteErrorBoundRequirement",
    "MaxPointwiseRelativeErrorBoundRequirement",
    "MaxPointwiseRangeRelativeErrorBoundRequirement",
    "MaxPointwiseQuadraticErrorBoundRequirement",
]


@dataclass(kw_only=True, slots=True)
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
    def get_config(self) -> Mapping[str, JSON]:
        return dict(kind=type(self).kind.get_config(), value=self.value)

    @override
    def humanise(self) -> str:
        return f"{_to_camel_case(type(self).kind)}({self.value})"


@dataclass(kw_only=True, slots=True)
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
    def get_config(self) -> Mapping[str, JSON]:
        return dict(kind=type(self).kind.get_config(), value=self.value)

    @override
    def humanise(self) -> str:
        return f"{_to_camel_case(type(self).kind)}({self.value})"


@dataclass(kw_only=True, slots=True)
class MaxPointwiseRangeRelativeErrorBoundRequirement(Requirement):
    kind: ClassVar[RequirementKind] = (
        RequirementKind.max_pointwise_range_relative_error_bound
    )
    value: int | float

    @override
    @classmethod
    def from_config(  # type: ignore
        cls,
        *,
        value: int | float,
        kind: Literal[
            "max-pointwise-range-relative-error-bound"
        ] = RequirementKind.max_pointwise_range_relative_error_bound.value,
    ) -> Self:
        return cls(value=_parse_number(value))

    @override
    def get_config(self) -> Mapping[str, JSON]:
        return dict(kind=type(self).kind.get_config(), value=self.value)

    @override
    def humanise(self) -> str:
        return f"{_to_camel_case(type(self).kind)}({self.value})"


@dataclass(kw_only=True, slots=True)
class MaxPointwiseQuadraticErrorBoundRequirement(Requirement):
    kind: ClassVar[RequirementKind] = (
        RequirementKind.max_pointwise_quadratic_error_bound
    )
    value: int | float
    minimum: int | float
    maximum: int | float

    @override
    @classmethod
    def from_config(  # type: ignore
        cls,
        *,
        value: int | float,
        minimum: int | float,
        maximum: int | float,
        kind: Literal[
            "max-pointwise-quadratic-error-bound"
        ] = RequirementKind.max_pointwise_quadratic_error_bound.value,
    ) -> Self:
        return cls(
            value=_parse_number(value),
            minimum=_parse_number(minimum),
            maximum=_parse_number(maximum),
        )

    @override
    def get_config(self) -> Mapping[str, JSON]:
        return dict(
            kind=type(self).kind.get_config(),
            value=self.value,
            minimum=self.minimum,
            maximum=self.maximum,
        )

    @override
    def humanise(self) -> str:
        return f"{_to_camel_case(type(self).kind)}({self.value}, minimum={self.minimum}, maximum={self.maximum})"
