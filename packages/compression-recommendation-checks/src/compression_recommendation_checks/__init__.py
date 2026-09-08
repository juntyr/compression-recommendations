from collections.abc import Collection
from typing import TypeVar, assert_never

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

__all__ = ["S", "T", "check_safety_requirements", "check_safety_requirement"]

S = TypeVar("S", bound=tuple[int, ...], covariant=True)
""" Any array shape (covariant). """

T = TypeVar("T", bound=np.number, covariant=True)
""" Any numpy [`number`][numpy.number] data type (covariant). """


def check_safety_requirements(
    *,
    original: np.ndarray[S, np.dtype[T]],
    reconstructed: np.ndarray[S, np.dtype[T]],
    requirements: Collection[Requirement],
) -> bool:
    return all(
        check_safety_requirement(
            original=original, reconstructed=reconstructed, requirement=requirement
        )
        for requirement in requirements
    )


def check_safety_requirement(
    *,
    original: np.ndarray[S, np.dtype[T]],
    reconstructed: np.ndarray[S, np.dtype[T]],
    requirement: Requirement,
) -> bool:
    return bool(
        np.all(
            _check_safety_requirement_pointwise(
                original=original, reconstructed=reconstructed, requirement=requirement
            )
        )
    )


@np.errstate(divide="ignore", over="ignore", under="ignore", invalid="ignore")
def _check_safety_requirement_pointwise(
    *,
    original: np.ndarray[S, np.dtype[T]],
    reconstructed: np.ndarray[S, np.dtype[T]],
    requirement: Requirement,
) -> np.ndarray[S, np.dtype[np.bool]]:
    ok: np.ndarray[S, np.dtype[np.bool]]

    match requirement.kind:
        case RequirementKind.any:
            assert isinstance(requirement, AnyRequirement)
            ok = np.zeros(original.shape, dtype=np.bool)
            for req in requirement.requirements:
                ok |= _check_safety_requirement_pointwise(
                    original=original, reconstructed=reconstructed, requirement=req
                )
            return ok
        case RequirementKind.all:
            assert isinstance(requirement, AllRequirements)
            ok = np.ones(original.shape, dtype=np.bool)
            for req in requirement.requirements:
                ok &= _check_safety_requirement_pointwise(
                    original=original, reconstructed=reconstructed, requirement=req
                )
            return ok
        case RequirementKind.max_pointwise_absolute_error_bound:
            assert isinstance(requirement, MaxPointwiseAbsoluteErrorBoundRequirement)
            # FIXME: rounding errors
            err: np.ndarray[S, np.dtype[T]] = np.abs(
                np.subtract(original, reconstructed)
            )
            bound = requirement.value
            ok = err <= bound
            ok |= original == reconstructed
            ok |= np.isnan(original) & np.isnan(reconstructed)
            return ok
        case RequirementKind.mean_absolute_error_bound:
            assert isinstance(requirement, MeanAbsoluteErrorBoundRequirement)
            # FIXME: rounding errors
            finite = np.isfinite(original)
            err = np.sum(np.abs(np.subtract(original, reconstructed)), where=finite)
            bound = requirement.value * np.count_nonzero(finite)
            ok = original == reconstructed
            ok |= np.isnan(original) & np.isnan(reconstructed)
            ok[finite] |= err <= bound
            return ok
        case RequirementKind.max_pointwise_relative_error_bound:
            assert isinstance(requirement, MaxPointwiseRelativeErrorBoundRequirement)
            # FIXME: rounding errors
            err: np.ndarray[S, np.dtype[T]] = np.abs(
                np.subtract(original, reconstructed)
            )
            bound = np.nan_to_num(np.abs(original) * requirement.value)
            ok = err <= bound
            ok |= original == reconstructed
            ok |= np.isnan(original) & np.isnan(reconstructed)
            return ok
        case RequirementKind.mean_relative_error_bound:
            assert isinstance(requirement, MeanRelativeErrorBoundRequirement)
            # FIXME: rounding errors
            finite = np.isfinite(original)
            err = np.sum(np.abs(np.subtract(original, reconstructed)), where=finite)
            bound = np.sum(
                np.nan_to_num(np.abs(original) * requirement.value), where=finite
            )
            ok = original == reconstructed
            ok |= np.isnan(original) & np.isnan(reconstructed)
            ok[finite] |= err <= bound
            return ok
        case RequirementKind.max_pointwise_range_relative_error_bound:
            assert isinstance(
                requirement, MaxPointwiseRangeRelativeErrorBoundRequirement
            )
            # FIXME: rounding errors
            err: np.ndarray[S, np.dtype[T]] = np.abs(
                np.subtract(original, reconstructed)
            )
            bound = (np.nanmax(original) - np.nanmin(original)) * requirement.value
            ok = err <= bound
            ok |= original == reconstructed
            ok |= np.isnan(original) & np.isnan(reconstructed)
            return ok
        case RequirementKind.mean_range_relative_error_bound:
            assert isinstance(requirement, MeanRangeRelativeErrorBoundRequirement)
            # FIXME: rounding errors
            finite = np.isfinite(original)
            err = np.sum(np.abs(np.subtract(original, reconstructed)), where=finite)
            bound = (
                (np.nanmax(original) - np.nanmin(original))
                * requirement.value
                * np.count_nonzero(finite)
            )
            ok = original == reconstructed
            ok |= np.isnan(original) & np.isnan(reconstructed)
            ok[finite] |= err <= bound
            return ok
        case RequirementKind.max_pointwise_quadratic_error_bound:
            assert isinstance(requirement, MaxPointwiseQuadraticErrorBoundRequirement)
            # FIXME: rounding errors
            x = -1 + 2 * (original - requirement.minimum) / (
                requirement.maximum - requirement.minimum
            )
            err: np.ndarray[S, np.dtype[T]] = np.abs(
                np.subtract(original, reconstructed)
            )
            bound = (1 - np.square(x)) * requirement.value
            ok = err <= bound
            ok |= original == reconstructed
            ok |= np.isnan(original) & np.isnan(reconstructed)
            return ok
        case RequirementKind.data_limits:
            assert isinstance(requirement, DataLimitsRequirement)
            # FIXME: rounding errors
            ok = np.ones(original.shape, dtype=np.bool)
            if requirement.minimum is not None:
                ok |= (reconstructed >= requirement.minimum) | ~(
                    original >= requirement.minimum
                )
            if requirement.maximum is not None:
                ok |= (reconstructed <= requirement.maximum) | ~(
                    original <= requirement.maximum
                )
            return ok
        case RequirementKind.isovalue:
            assert isinstance(requirement, IsovalueRequirement)
            # FIXME: rounding errors
            ok = np.ones(original.shape, dtype=np.bool)
            ok &= (original < requirement.value) == (reconstructed < requirement.value)
            ok &= (original == requirement.value) == (
                reconstructed == requirement.value
            )
            ok &= (original > requirement.value) == (reconstructed > requirement.value)
            return ok
        case RequirementKind.missing_value:
            assert isinstance(requirement, MissingValueRequirement)
            # FIXME: rounding errors
            if np.isnan(requirement.value):
                return np.isnan(original) == np.isnan(reconstructed)
            return (original == requirement.value) == (
                reconstructed == requirement.value
            )
        case RequirementKind.lossless:
            assert isinstance(requirement, LosslessRequirement)
            return _as_bits(original) == _as_bits(reconstructed)
        case _:
            assert_never(requirement.kind)


def _as_bits(
    a: np.ndarray[S, np.dtype[T]],
) -> np.ndarray[S, np.dtype[np.unsignedinteger]]:
    return a.view(a.dtype.str.replace("f", "u").replace("i", "u"))
