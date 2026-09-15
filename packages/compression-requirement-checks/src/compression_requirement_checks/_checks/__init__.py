from typing import assert_never

import numpy as np
from compression_recommendations.requirements.abc import Requirement
from compression_recommendations.requirements.combinators import (
    AllRequirements,
    AnyRequirement,
)
from compression_recommendations.requirements.error_bounds.max import (
    MaxPointwiseAbsoluteErrorBoundRequirement,
    MaxPointwiseQuadraticErrorBoundRequirement,
    MaxPointwiseRangeRelativeErrorBoundRequirement,
    MaxPointwiseRelativeErrorBoundRequirement,
)
from compression_recommendations.requirements.error_bounds.mean import (
    MeanAbsoluteErrorBoundRequirement,
    MeanRangeRelativeErrorBoundRequirement,
    MeanRelativeErrorBoundRequirement,
)
from compression_recommendations.requirements.isovalue import IsovalueRequirement
from compression_recommendations.requirements.kind import RequirementKind
from compression_recommendations.requirements.limits import DataLimitsRequirement
from compression_recommendations.requirements.lossless import LosslessRequirement
from compression_recommendations.requirements.missing import MissingValueRequirement

from .._convert import _get_lossless_floating_point_type
from ..typing import S_co, T_co
from .combinators import _check_all, _check_any
from .error_bounds.max import (
    _check_maximum_pointwise_absolute_error_bound,
    _check_maximum_pointwise_quadratic_error_bound,
    _check_maximum_pointwise_range_relative_error_bound,
    _check_maximum_pointwise_relative_error_bound,
)
from .error_bounds.mean import (
    _check_mean_absolute_error_bound,
    _check_mean_range_relative_error_bound,
    _check_mean_relative_error_bound,
)
from .isovalue import _check_isovalue
from .limits import _check_data_limits
from .lossless import _check_lossless
from .missing import _check_missing_value

__all__ = ["_check_safety_requirement_pointwise"]


def _check_safety_requirement_pointwise(
    *,
    original: np.ndarray[S_co, np.dtype[T_co]],
    reconstructed: np.ndarray[S_co, np.dtype[T_co]],
    requirement: Requirement,
) -> np.ndarray[S_co, np.dtype[np.bool]]:
    match requirement.kind:
        case RequirementKind.any:
            assert isinstance(requirement, AnyRequirement)
            return _check_any(
                original=original,
                reconstructed=reconstructed,
                requirements=requirement.requirements,
            )
        case RequirementKind.all:
            assert isinstance(requirement, AllRequirements)
            return _check_all(
                original=original,
                reconstructed=reconstructed,
                requirements=requirement.requirements,
            )
        case RequirementKind.max_pointwise_absolute_error_bound:
            assert isinstance(requirement, MaxPointwiseAbsoluteErrorBoundRequirement)
            return _check_maximum_pointwise_absolute_error_bound(
                original=original,
                reconstructed=reconstructed,
                eb_abs=requirement.value,
                ftype=_get_lossless_floating_point_type(original.dtype),
            )
        case RequirementKind.mean_absolute_error_bound:
            assert isinstance(requirement, MeanAbsoluteErrorBoundRequirement)
            return _check_mean_absolute_error_bound(
                original=original,
                reconstructed=reconstructed,
                eb_mean_abs=requirement.value,
                ftype=_get_lossless_floating_point_type(original.dtype),
            )
        case RequirementKind.max_pointwise_relative_error_bound:
            assert isinstance(requirement, MaxPointwiseRelativeErrorBoundRequirement)
            return _check_maximum_pointwise_relative_error_bound(
                original=original,
                reconstructed=reconstructed,
                eb_rel=requirement.value,
                ftype=_get_lossless_floating_point_type(original.dtype),
            )
        case RequirementKind.mean_relative_error_bound:
            assert isinstance(requirement, MeanRelativeErrorBoundRequirement)
            return _check_mean_relative_error_bound(
                original=original,
                reconstructed=reconstructed,
                eb_mean_rel=requirement.value,
                ftype=_get_lossless_floating_point_type(original.dtype),
            )
        case RequirementKind.max_pointwise_range_relative_error_bound:
            assert isinstance(
                requirement, MaxPointwiseRangeRelativeErrorBoundRequirement
            )
            return _check_maximum_pointwise_range_relative_error_bound(
                original=original,
                reconstructed=reconstructed,
                eb_range_rel=requirement.value,
                ftype=_get_lossless_floating_point_type(original.dtype),
            )
        case RequirementKind.mean_range_relative_error_bound:
            assert isinstance(requirement, MeanRangeRelativeErrorBoundRequirement)
            return _check_mean_range_relative_error_bound(
                original=original,
                reconstructed=reconstructed,
                eb_mean_range_rel=requirement.value,
                ftype=_get_lossless_floating_point_type(original.dtype),
            )
        case RequirementKind.max_pointwise_quadratic_error_bound:
            assert isinstance(requirement, MaxPointwiseQuadraticErrorBoundRequirement)
            return _check_maximum_pointwise_quadratic_error_bound(
                original=original,
                reconstructed=reconstructed,
                eb_qua=requirement.value,
                minimum=requirement.minimum,
                maximum=requirement.maximum,
                ftype=_get_lossless_floating_point_type(original.dtype),
            )
        case RequirementKind.data_limits:
            assert isinstance(requirement, DataLimitsRequirement)
            return _check_data_limits(
                original=original,
                reconstructed=reconstructed,
                minimum=requirement.minimum,
                maximum=requirement.maximum,
                ftype=_get_lossless_floating_point_type(original.dtype),
            )
        case RequirementKind.isovalue:
            assert isinstance(requirement, IsovalueRequirement)
            return _check_isovalue(
                original=original,
                reconstructed=reconstructed,
                isovalue=requirement.value,
                ftype=_get_lossless_floating_point_type(original.dtype),
            )
        case RequirementKind.missing_value:
            assert isinstance(requirement, MissingValueRequirement)
            return _check_missing_value(
                original=original,
                reconstructed=reconstructed,
                missing_value=requirement.value,
                ftype=_get_lossless_floating_point_type(original.dtype),
            )
        case RequirementKind.lossless:
            assert isinstance(requirement, LosslessRequirement)
            return _check_lossless(original=original, reconstructed=reconstructed)
        case _:
            assert_never(requirement.kind)
