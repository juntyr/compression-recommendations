"""
Enumeration over all requirement kinds.
"""

from enum import StrEnum
from typing import TYPE_CHECKING, Self, assert_never

if TYPE_CHECKING:
    from .abc import Requirement

from ..typing import JSON

__all__ = ["RequirementKind"]


class RequirementKind(StrEnum):
    """
    Enumeration over all requirement kinds.
    """

    any = "any"
    """ See the [`AnyRequirement`][....combinators.AnyRequirement]. """

    all = "all"
    """ See the [`AllRequirements`][....combinators.AllRequirements]. """

    max_pointwise_absolute_error_bound = "max-pointwise-absolute-error-bound"
    """ See the [`MaxPointwiseAbsoluteErrorBoundRequirement`][....error_bounds.max.MaxPointwiseAbsoluteErrorBoundRequirement]. """

    mean_absolute_error_bound = "mean-absolute-error-bound"
    """ See the [`MeanAbsoluteErrorBoundRequirement`][....error_bounds.mean.MeanAbsoluteErrorBoundRequirement]. """

    max_pointwise_relative_error_bound = "max-pointwise-relative-error-bound"
    """ See the [`MaxPointwiseRelativeErrorBoundRequirement`][....error_bounds.max.MaxPointwiseRelativeErrorBoundRequirement]. """

    mean_relative_error_bound = "mean-relative-error-bound"
    """ See the [`MeanRelativeErrorBoundRequirement`][....error_bounds.mean.MeanRelativeErrorBoundRequirement]. """

    max_pointwise_range_relative_error_bound = (
        "max-pointwise-range-relative-error-bound"
    )
    """ See the [`MaxPointwiseRangeRelativeErrorBoundRequirement`][....error_bounds.max.MaxPointwiseRangeRelativeErrorBoundRequirement]. """

    mean_range_relative_error_bound = "mean-range-relative-error-bound"
    """ See the [`MeanRangeRelativeErrorBoundRequirement`][....error_bounds.mean.MeanRangeRelativeErrorBoundRequirement]. """

    max_pointwise_quadratic_error_bound = "max-pointwise-quadratic-error-bound"
    """ See the [`MaxPointwiseQuadraticErrorBoundRequirement`][....error_bounds.max.MaxPointwiseQuadraticErrorBoundRequirement]. """

    data_limits = "data-limits"
    """ See the [`DataLimitsRequirement`][....limits.DataLimitsRequirement]. """

    isovalue = "isovalue"
    """ See the [`IsovalueRequirement`][....isovalue.IsovalueRequirement]. """

    missing_value = "missing-value"
    """ See the [`MissingValueRequirement`][....missing.MissingValueRequirement]. """

    lossless = "lossless"
    """ See the [`LosslessRequirement`][....lossless.LosslessRequirement]. """

    @property
    def cls(self) -> type["Requirement"]:
        """
        The concrete requirement class associated with this requirement kind.
        """

        match self:
            case RequirementKind.any:
                from .combinators import AnyRequirement  # noqa: PLC0415

                return AnyRequirement
            case RequirementKind.all:
                from .combinators import AllRequirements  # noqa: PLC0415

                return AllRequirements
            case RequirementKind.max_pointwise_absolute_error_bound:
                from .error_bounds.max import (  # noqa: PLC0415
                    MaxPointwiseAbsoluteErrorBoundRequirement,
                )

                return MaxPointwiseAbsoluteErrorBoundRequirement
            case RequirementKind.mean_absolute_error_bound:
                from .error_bounds.mean import (  # noqa: PLC0415
                    MeanAbsoluteErrorBoundRequirement,
                )

                return MeanAbsoluteErrorBoundRequirement
            case RequirementKind.max_pointwise_relative_error_bound:
                from .error_bounds.max import (  # noqa: PLC0415
                    MaxPointwiseRelativeErrorBoundRequirement,
                )

                return MaxPointwiseRelativeErrorBoundRequirement
            case RequirementKind.mean_relative_error_bound:
                from .error_bounds.mean import (  # noqa: PLC0415
                    MeanRelativeErrorBoundRequirement,
                )

                return MeanRelativeErrorBoundRequirement
            case RequirementKind.max_pointwise_range_relative_error_bound:
                from .error_bounds.max import (  # noqa: PLC0415
                    MaxPointwiseRangeRelativeErrorBoundRequirement,
                )

                return MaxPointwiseRangeRelativeErrorBoundRequirement
            case RequirementKind.mean_range_relative_error_bound:
                from .error_bounds.mean import (  # noqa: PLC0415
                    MeanRangeRelativeErrorBoundRequirement,
                )

                return MeanRangeRelativeErrorBoundRequirement
            case RequirementKind.max_pointwise_quadratic_error_bound:
                from .error_bounds.max import (  # noqa: PLC0415
                    MaxPointwiseQuadraticErrorBoundRequirement,
                )

                return MaxPointwiseQuadraticErrorBoundRequirement
            case RequirementKind.data_limits:
                from .limits import DataLimitsRequirement  # noqa: PLC0415

                return DataLimitsRequirement
            case RequirementKind.isovalue:
                from .isovalue import IsovalueRequirement  # noqa: PLC0415

                return IsovalueRequirement
            case RequirementKind.missing_value:
                from .missing import MissingValueRequirement  # noqa: PLC0415

                return MissingValueRequirement
            case RequirementKind.lossless:
                from .lossless import LosslessRequirement  # noqa: PLC0415

                return LosslessRequirement
            case _:
                assert_never(self)

    @classmethod
    def from_config(cls, kind: str) -> Self:
        """
        Construct the requirement kind from its configuration.

        Parameters
        ----------
        kind : str
            The requirement kind name.

        Returns
        -------
        kind : Self
            The instantiated requirement kind.
        """

        return cls[kind.replace("-", "_")]

    def get_config(self) -> JSON:
        """
        Get the configuration of this requirement kind.

        Returns
        -------
        config : JSIN
            Configuration in JSON format.
        """

        return self.value
