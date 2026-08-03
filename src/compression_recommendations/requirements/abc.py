"""
Abstract base class for requirements.
"""

from abc import ABC
from typing import ClassVar, Self, assert_never

from typing_extensions import override  # MSPV 3.12

from ..config import Config
from ..typing import JSON
from .kind import RequirementKind

__all__ = ["Requirement"]


class Requirement(Config, ABC):
    __slots__: tuple[str, ...] = ("kind",)

    kind: ClassVar[RequirementKind]

    @override
    @classmethod
    def from_config(cls, *, kind: str, **kwargs: JSON) -> Self:  # type: ignore
        from .combinators import AllRequirements, AnyRequirement  # noqa: PLC0415
        from .error_bounds.max import (  # noqa: PLC0415
            MaxPointwiseAbsoluteErrorBoundRequirement,
            MaxPointwiseRelativeErrorBoundRequirement,
        )
        from .error_bounds.mean import (  # noqa: PLC0415
            MeanAbsoluteErrorBoundRequirement,
            MeanRelativeErrorBoundRequirement,
        )
        from .isovalue import IsovalueRequirement  # noqa: PLC0415
        from .limits import DataLimitsRequirement  # noqa: PLC0415

        kind_ = RequirementKind.from_config(kind)
        match kind_:
            case RequirementKind.any:
                return AnyRequirement.from_config(
                    **kwargs  # type: ignore
                )
            case RequirementKind.all:
                return AllRequirements.from_config(
                    **kwargs  # type: ignore
                )
            case RequirementKind.max_pointwise_absolute_error_bound:
                return MaxPointwiseAbsoluteErrorBoundRequirement.from_config(
                    **kwargs  # type: ignore
                )
            case RequirementKind.mean_absolute_error_bound:
                return MeanAbsoluteErrorBoundRequirement.from_config(
                    **kwargs  # type: ignore
                )
            case RequirementKind.max_pointwise_relative_error_bound:
                return MaxPointwiseRelativeErrorBoundRequirement.from_config(
                    **kwargs  # type: ignore
                )
            case RequirementKind.mean_relative_error_bound:
                return MeanRelativeErrorBoundRequirement.from_config(
                    **kwargs  # type: ignore
                )
            case RequirementKind.data_limits:
                return DataLimitsRequirement.from_config(
                    **kwargs  # type: ignore
                )
            case RequirementKind.isovalue:
                return IsovalueRequirement.from_config(
                    **kwargs  # type: ignore
                )
            case _:
                assert_never(kind_)
