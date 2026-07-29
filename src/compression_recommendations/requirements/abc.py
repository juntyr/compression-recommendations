from abc import ABC
from typing import ClassVar, Self, assert_never, override

from ..config import Config
from ..typing import JSON
from .kind import RequirementKind

__all__ = ["Requirement"]


class Requirement(Config, ABC):
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
            MeanPointwiseAbsoluteErrorBoundRequirement,
            MeanPointwiseRelativeErrorBoundRequirement,
        )

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
            case RequirementKind.mean_pointwise_absolute_error_bound:
                return MeanPointwiseAbsoluteErrorBoundRequirement.from_config(
                    **kwargs  # type: ignore
                )
            case RequirementKind.max_pointwise_relative_error_bound:
                return MaxPointwiseRelativeErrorBoundRequirement.from_config(
                    **kwargs  # type: ignore
                )
            case RequirementKind.mean_pointwise_relative_error_bound:
                return MeanPointwiseRelativeErrorBoundRequirement.from_config(
                    **kwargs  # type: ignore
                )
            case _:
                assert_never(kind_)
