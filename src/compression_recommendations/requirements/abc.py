from abc import ABC
from typing import ClassVar, Self, assert_never

from typing_extensions import override  # MSPV 3.12

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
        from .extrema import (  # noqa: PLC0415
            GlobalMaximumRequirement,
            GlobalMinimumRequirement,
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
            case RequirementKind.global_minimum:
                return GlobalMinimumRequirement.from_config(
                    **kwargs  # type: ignore
                )
            case RequirementKind.global_maximum:
                return GlobalMaximumRequirement.from_config(
                    **kwargs  # type: ignore
                )
            case _:
                assert_never(kind_)
