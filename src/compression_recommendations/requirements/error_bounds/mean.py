from dataclasses import dataclass
from typing import ClassVar, Literal, Self

from typing_extensions import override  # MSPV 3.12

from ...typing import JSON
from ..abc import Requirement
from ..kind import RequirementKind

__all__ = [
    "MeanPointwiseAbsoluteErrorBoundRequirement",
    "MeanPointwiseRelativeErrorBoundRequirement",
]


@dataclass(kw_only=True)
class MeanPointwiseAbsoluteErrorBoundRequirement(Requirement):
    kind: ClassVar[RequirementKind] = (
        RequirementKind.mean_pointwise_absolute_error_bound
    )
    value: int | float

    @override
    @classmethod
    def from_config(  # type: ignore
        cls,
        *,
        value: int | float,
        kind: Literal[
            "mean-pointwise-absolute-error-bound"
        ] = RequirementKind.mean_pointwise_absolute_error_bound.value,
    ) -> Self:
        return cls(value=value)

    @override
    def get_config(self) -> JSON:
        return dict(kind=type(self).kind.get_config(), value=self.value)


@dataclass(kw_only=True)
class MeanPointwiseRelativeErrorBoundRequirement(Requirement):
    kind: ClassVar[RequirementKind] = (
        RequirementKind.mean_pointwise_relative_error_bound
    )
    value: int | float

    @override
    @classmethod
    def from_config(  # type: ignore
        cls,
        *,
        value: int | float,
        kind: Literal[
            "mean-pointwise-relative-error-bound"
        ] = RequirementKind.mean_pointwise_relative_error_bound.value,
    ) -> Self:
        return cls(value=value)

    @override
    def get_config(self) -> JSON:
        return dict(kind=type(self).kind.get_config(), value=self.value)
