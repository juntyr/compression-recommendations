from collections.abc import Mapping
from typing import TYPE_CHECKING, assert_never, cast

from compression_recommendations import Recommendations
from compression_recommendations.requirements.abc import Requirement
from compression_recommendations.requirements.kind import RequirementKind
from compression_safeguards.api import Safeguards
from compression_safeguards.safeguards.abc import Safeguard
from compression_safeguards.safeguards.combinators.all import AllSafeguards
from compression_safeguards.safeguards.combinators.any import AnySafeguard
from compression_safeguards.safeguards.eb import ErrorBound
from compression_safeguards.safeguards.pointwise.abc import PointwiseSafeguard
from compression_safeguards.safeguards.pointwise.eb import ErrorBoundSafeguard
from compression_safeguards.safeguards.pointwise.sign import SignPreservingSafeguard
from compression_safeguards.safeguards.stencil.abc import StencilSafeguard

if TYPE_CHECKING:
    from compression_recommendations.requirements.combinators import (
        AllRequirements,
        AnyRequirement,
    )
    from compression_recommendations.requirements.error_bounds.max import (
        MaxPointwiseAbsoluteErrorBoundRequirement,
        MaxPointwiseRelativeErrorBoundRequirement,
    )
    from compression_recommendations.requirements.error_bounds.mean import (
        MeanAbsoluteErrorBoundRequirement,
        MeanRelativeErrorBoundRequirement,
    )
    from compression_recommendations.requirements.extrema import (
        GlobalMaximumRequirement,
        GlobalMinimumRequirement,
    )
    from compression_recommendations.requirements.isovalue import IsovalueRequirement

__all__ = [
    "recommended_safeguards_for",
    "search_for_recommended_safeguards",
    "safeguard_for_requirement",
]


def recommended_safeguards_for(
    *, markers: Mapping[str, None | bool | int | float | str]
) -> Safeguards:
    return search_for_recommended_safeguards(
        recommendations=cast("Recommendations", Recommendations.provide),
        markers=markers,
    )


def search_for_recommended_safeguards(
    *,
    recommendations: Recommendations,
    markers: Mapping[str, None | bool | int | float | str],
) -> Safeguards:
    return Safeguards(
        safeguards=[
            safeguard_for_requirement(requirement)
            for requirement in recommendations.search(markers=markers)
        ]
    )


def safeguard_for_requirement(requirement: Requirement) -> Safeguard:
    return _safeguard_for_requirement(requirement)


def _safeguard_for_requirement(
    requirement: Requirement,
) -> PointwiseSafeguard | StencilSafeguard:
    match requirement.kind:
        case RequirementKind.any:
            return AnySafeguard(  # type: ignore
                safeguards=[
                    _safeguard_for_requirement(req)
                    for req in cast("AnyRequirement", requirement).requirements
                ]
            )
        case RequirementKind.all:
            return AllSafeguards(  # type: ignore
                safeguards=[
                    _safeguard_for_requirement(req)
                    for req in cast("AllRequirements", requirement).requirements
                ]
            )
        case RequirementKind.max_pointwise_absolute_error_bound:
            return ErrorBoundSafeguard(
                type=ErrorBound.abs,
                eb=cast("MaxPointwiseAbsoluteErrorBoundRequirement", requirement).value,
            )
        case RequirementKind.mean_absolute_error_bound:
            # conservatively bound the pointwise absolute error instead
            return ErrorBoundSafeguard(
                type=ErrorBound.abs,
                eb=cast("MeanAbsoluteErrorBoundRequirement", requirement).value,
            )
        case RequirementKind.max_pointwise_relative_error_bound:
            return ErrorBoundSafeguard(
                type=ErrorBound.rel,
                eb=cast("MaxPointwiseRelativeErrorBoundRequirement", requirement).value,
            )
        case RequirementKind.mean_relative_error_bound:
            # conservatively bound the pointwise absolute error instead
            return ErrorBoundSafeguard(
                type=ErrorBound.abs,
                eb=cast("MeanRelativeErrorBoundRequirement", requirement).value,
            )
        case RequirementKind.global_minimum:
            # slightly conservative since global minimum will be kept exactly
            return SignPreservingSafeguard(
                offset=cast("GlobalMinimumRequirement", requirement).value
            )
            # TODO: switch to pointwise QoI with early-bound param support
            # return PointwiseQuantityOfInterestErrorBoundSafeguard(
            #     qoi='x >= c["minimum"]',
            #     type="abs",
            #     eb=0,
            #     early_bound=dict(
            #         minimum=cast("GlobalMinimumRequirement", requirement).value
            #     ),
            # )
        case RequirementKind.global_maximum:
            # slightly conservative since global maximum will be kept exactly
            return SignPreservingSafeguard(
                offset=cast("GlobalMaximumRequirement", requirement).value
            )
            # TODO: switch to pointwise QoI with early-bound param support
            # return PointwiseQuantityOfInterestErrorBoundSafeguard(
            #     qoi='x <= c["maximum"]',
            #     type="abs",
            #     eb=0,
            #     early_bound=dict(
            #         maximum=cast("GlobalMaximumRequirement", requirement).value
            #     ),
            # )
        case RequirementKind.isovalue:
            return SignPreservingSafeguard(
                offset=cast("IsovalueRequirement", requirement).value
            )
        case _:
            assert_never(requirement.kind)
