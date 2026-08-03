from collections.abc import Collection, Mapping
from typing import assert_never, cast

from compression_recommendations import Recommendations
from compression_recommendations.requirements.abc import Requirement
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
from compression_recommendations.requirements.isovalue import IsovalueRequirement
from compression_recommendations.requirements.kind import RequirementKind
from compression_recommendations.requirements.limits import DataLimitsRequirement
from compression_safeguards.api import Safeguards
from compression_safeguards.safeguards.abc import Safeguard
from compression_safeguards.safeguards.combinators.all import AllSafeguards
from compression_safeguards.safeguards.combinators.any import AnySafeguard
from compression_safeguards.safeguards.eb import ErrorBound
from compression_safeguards.safeguards.pointwise.abc import PointwiseSafeguard
from compression_safeguards.safeguards.pointwise.eb import ErrorBoundSafeguard
from compression_safeguards.safeguards.pointwise.sign import SignPreservingSafeguard
from compression_safeguards.safeguards.stencil.abc import StencilSafeguard

__all__ = [
    "recommended_safeguards_for",
    "search_for_recommended_safeguards",
    "safeguards_for_requirement",
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
            sg
            for requirement in recommendations.search(markers=markers)
            for sg in safeguards_for_requirement(requirement)
        ]
    )


def safeguards_for_requirement(requirement: Requirement) -> Collection[Safeguard]:
    return _safeguards_for_requirement(requirement)


def _safeguards_for_requirement(
    requirement: Requirement,
) -> Collection[PointwiseSafeguard | StencilSafeguard]:
    match requirement.kind:
        case RequirementKind.any:
            assert isinstance(requirement, AnyRequirement)
            return [
                AnySafeguard(  # type: ignore
                    safeguards=[
                        sg
                        for req in requirement.requirements
                        for sg in _safeguards_for_requirement(req)
                    ]
                )
            ]
        case RequirementKind.all:
            assert isinstance(requirement, AllRequirements)
            return [
                AllSafeguards(  # type: ignore
                    safeguards=[
                        sg
                        for req in requirement.requirements
                        for sg in _safeguards_for_requirement(req)
                    ]
                )
            ]
        case RequirementKind.max_pointwise_absolute_error_bound:
            assert isinstance(requirement, MaxPointwiseAbsoluteErrorBoundRequirement)
            return [ErrorBoundSafeguard(type=ErrorBound.abs, eb=requirement.value)]
        case RequirementKind.mean_absolute_error_bound:
            assert isinstance(requirement, MeanAbsoluteErrorBoundRequirement)
            # conservatively bound the pointwise absolute error instead
            return [ErrorBoundSafeguard(type=ErrorBound.abs, eb=requirement.value)]
        case RequirementKind.max_pointwise_relative_error_bound:
            assert isinstance(requirement, MaxPointwiseRelativeErrorBoundRequirement)
            return [ErrorBoundSafeguard(type=ErrorBound.rel, eb=requirement.value)]
        case RequirementKind.mean_relative_error_bound:
            assert isinstance(requirement, MeanRelativeErrorBoundRequirement)
            # conservatively bound the pointwise absolute error instead
            return [ErrorBoundSafeguard(type=ErrorBound.abs, eb=requirement.value)]
        case RequirementKind.data_limits:
            assert isinstance(requirement, DataLimitsRequirement)
            # slightly conservative since global minimum will be kept exactly
            safeguards = []
            if requirement.minimum is not None:
                safeguards.append(SignPreservingSafeguard(offset=requirement.minimum))
            if requirement.maximum is not None:
                safeguards.append(SignPreservingSafeguard(offset=requirement.maximum))
            return safeguards
            # TODO: switch to pointwise QoI with early-bound param support
            # if requirement.minimum is not None:
            #     safeguards.append(
            #         PointwiseQuantityOfInterestErrorBoundSafeguard(
            #             qoi='x >= c["minimum"]',
            #             type="abs",
            #             eb=0,
            #             early_bound=dict(minimum=requirement.minimum),
            #         )
            #     )
            # if requirement.maximum is not None:
            #     safeguards.append(
            #         PointwiseQuantityOfInterestErrorBoundSafeguard(
            #             qoi='x <= c["maximum"]',
            #             type="abs",
            #             eb=0,
            #             early_bound=dict(maximum=requirement.maximum),
            #         )
            #     )
        case RequirementKind.isovalue:
            assert isinstance(requirement, IsovalueRequirement)
            return [SignPreservingSafeguard(offset=requirement.value)]
        case _:
            assert_never(requirement.kind)
