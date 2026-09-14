"""
# Recommended Compression Safeguards for Safe Lossy Compression of weather and climate data

What lossy compression is safe when using lossy compression on weather and
climate data?

This package translates compression safety
[`Requirement`][compression_recommendations.requirements.abc.Requirement]s
into compression
[`Safeguards`][compression_safeguards.api.Safeguards], which can be wrapped
around any compressor to guarantee that the requirements are fulfilled.

The recommended safeguards for a given use case can be found via the three
provided functions:

- [`recommended_safeguards_for`][.recommended_safeguards_for] finds the
  [community-recommended][compression_recommendations.Recommendations.provide]
  safeguards,
- [`search_for_recommended_safeguards`][.search_for_recommended_safeguards]
  finds the safeguards recommended by the given
  [`Recommendations`][compression_recommendations.Recommendations], and
- [`safeguards_for_requirement`][.safeguards_for_requirement] translates a
  single
  [`Requirement`][compression_recommendations.requirements.abc.Requirement]
  into a collection of
  [`Safeguard`][compression_safeguards.safeguards.abc.Safeguard]s.
"""

from collections.abc import Collection, Mapping
from typing import assert_never

from compression_recommendations import Recommendations
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
from compression_safeguards.api import Safeguards
from compression_safeguards.safeguards.abc import Safeguard
from compression_safeguards.safeguards.combinators.all import AllSafeguards
from compression_safeguards.safeguards.combinators.any import AnySafeguard
from compression_safeguards.safeguards.combinators.everywhere import EverywhereSafeguard
from compression_safeguards.safeguards.eb import ErrorBound
from compression_safeguards.safeguards.pointwise.abc import PointwiseSafeguard
from compression_safeguards.safeguards.pointwise.eb import ErrorBoundSafeguard
from compression_safeguards.safeguards.pointwise.lossless import LosslessSafeguard
from compression_safeguards.safeguards.pointwise.qoi.eb import (
    PointwiseQuantityOfInterestErrorBoundSafeguard,
)
from compression_safeguards.safeguards.pointwise.same import EquivalentValueSafeguard
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
    """
    Find the [community-recommended][compression_recommendations.Recommendations.provide] safeguards for the given use case, identified by the `markers`.

    Parameters
    ----------
    markers : Mapping[str, None | bool | int | float | str]
        The markers that identify the use case, e.g. the variable, for which
        safeguards are produced.

        Please refer to
        [`compression_recommendations.Recommendations.search`][compression_recommendations.Recommendations.search]
        for an explanation of the markers.

    Returns
    -------
    safeguards : Safeguards
        The safeguards that guarantee that the recommended safety requirements
        are met.

    Raises
    ------
    KeyError
        if no recommendations could be found for the provided `markers`.

    Examples
    -------
    ```py
    import compression_safeguards_recommendations

    compression_safeguards_recommendations.recommended_safeguards_for(
        markers={"cf-short-name": "u10", "level-kind": "single"},
    )
    ```
    finds the recommended safeguards for 10 metre u wind.
    """

    return search_for_recommended_safeguards(
        recommendations=Recommendations.provide,
        markers=markers,
    )


def search_for_recommended_safeguards(
    *,
    recommendations: Recommendations,
    markers: Mapping[str, None | bool | int | float | str],
) -> Safeguards:
    """
    Find the safeguards recommended by the given `recommendations` for the given use case, identified by the `markers`.

    Parameters
    ----------
    recommendations : Recommendations
        The recommendations that will be searched for the safety requirements.
    markers : Mapping[str, None | bool | int | float | str]
        The markers that identify the use case, e.g. the variable, for which
        safeguards are produced.

        Please refer to
        [`compression_recommendations.Recommendations.search`][compression_recommendations.Recommendations.search]
        for an explanation of the markers.

    Returns
    -------
    safeguards : Safeguards
        The safeguards that guarantee that the recommended safety requirements
        are met.

    Raises
    ------
    KeyError
        if no `recommendations` could be found for the provided `markers`.

    Examples
    --------
    ```py
    import compression_safeguards_recommendations
    from compression_recommendations import Recommendations

    compression_safeguards_recommendations.search_for_recommended_safeguards(
        recommendations=Recommendations.provide,
        markers={"cf-short-name": "u10", "level-kind": "single"},
    )
    ```
    finds the recommended safeguards for 10 metre u wind.
    """

    return Safeguards(
        safeguards=[
            sg
            for requirement in recommendations.search(markers=markers)
            for sg in safeguards_for_requirement(requirement)
        ]
    )


def safeguards_for_requirement(requirement: Requirement) -> Collection[Safeguard]:
    """
    Translate the given `requirement` into a collection of safeguards.

    Parameters
    ----------
    requirement : Requirement
        The safety requirement to translate into safeguards.

    Returns
    -------
    safeguards : Collection[Safeguard]
        The safeguards required to guarantee that the `requirement` is met.
    """

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
            (safeguard,) = _safeguards_for_requirement(
                MaxPointwiseAbsoluteErrorBoundRequirement(value=requirement.value)
            )
            return [EverywhereSafeguard(safeguard=safeguard)]
        case RequirementKind.max_pointwise_relative_error_bound:
            assert isinstance(requirement, MaxPointwiseRelativeErrorBoundRequirement)
            return [ErrorBoundSafeguard(type=ErrorBound.rel, eb=requirement.value)]
        case RequirementKind.mean_relative_error_bound:
            assert isinstance(requirement, MeanRelativeErrorBoundRequirement)
            # conservatively bound the pointwise relative error instead
            (safeguard,) = _safeguards_for_requirement(
                MaxPointwiseRelativeErrorBoundRequirement(value=requirement.value)
            )
            return [EverywhereSafeguard(safeguard=safeguard)]
        case RequirementKind.max_pointwise_range_relative_error_bound:
            assert isinstance(
                requirement, MaxPointwiseRangeRelativeErrorBoundRequirement
            )
            return [
                PointwiseQuantityOfInterestErrorBoundSafeguard(
                    qoi="""
                    # scale x to be relative to $x_finite_max - $x_finite_min
                    # nudge to conservatively inflate the error so that
                    #  rounding errors cannot cause a violation
                    # TODO: use operations with rounding modes instead
                    v["x_finite_range"] = nextafter(c["$x_finite_max"] - c["$x_finite_min"], 0);
                    v["x_rel"] = nextafter(x / v["x_finite_range"], Inf);
                    v["x_orig_rel"] = nextafter(c["$x"] / v["x_finite_range"], Inf);

                    return where(
                        all([isfinite(v["x_orig_rel"]), not(c["eb_is_zero"])]),

                        # if $x_rel is finite, use it to fulfil the range-relative
                        # error bound, as long as eb_range_rel > 0:
                        #   |x - $x| <= eb_range_rel * x_finite_range
                        #   |x - $x| / x_finite_range <= eb_range_rel
                        #   | (x / x_finite_range) - ($x / x_finite_range) | <= eb_range_rel
                        #   |qoi(x) - qoi($x)| <= eb_range_rel
                        #     with qoi(x) = x / x_finite_range
                        v["x_rel"],

                        # otherwise, if $x could not be normalised,
                        # ensure instead that x == $x
                        where(
                            isnan(c["$x"]),

                            # use the fact that NaN results will always be
                            # preserved, and so if $x is NaN and we return x
                            # then the error bound can only be for x is NaN
                            x,

                            # use the fact that the error bound will always be
                            # finite, and so the error bound can only be met if
                            # x == $x, since this is true for $x
                            where(x == c["$x"], Inf, 0),
                        ),
                    );
                    """,  # type: ignore
                    type=ErrorBound.abs,
                    eb=requirement.value,
                    early_bound=dict(eb_is_zero=requirement.value == 0),
                )
            ]
        case RequirementKind.mean_range_relative_error_bound:
            assert isinstance(requirement, MeanRangeRelativeErrorBoundRequirement)
            # conservatively bound the pointwise range-relative error instead
            (safeguard,) = _safeguards_for_requirement(
                MaxPointwiseRangeRelativeErrorBoundRequirement(value=requirement.value)
            )
            return [EverywhereSafeguard(safeguard=safeguard)]
        case RequirementKind.max_pointwise_quadratic_error_bound:
            assert isinstance(requirement, MaxPointwiseQuadraticErrorBoundRequirement)
            return [
                PointwiseQuantityOfInterestErrorBoundSafeguard(
                    qoi="""
                    # scale $x to [-1; +1] via ($x - min / (max - min)) * 2 - 1
                    # nudge at every step to conservatively inflate the error
                    #  so that rounding errors should not cause a violation
                    # TODO: use operations with rounding modes instead
                    v["x_2"] = (c["$x"] - c["minimum"]) / (c["maximum"] - c["minimum"]);
                    v["x_1"] = where(
                        v["x_2"] <= 0.5,
                        # FIXME: no double nudging
                        nextafter(nextafter(v["x_2"], 0), 0),
                        nextafter(nextafter(v["x_2"], 1), 1),
                    );
                    v["x0"] = v["x_1"] * 2 - 1;
                    v["x1"] = where(
                        v["x0"] <= 0,
                        nextafter(v["x0"], -1),
                        nextafter(v["x0"], +1),
                    );

                    return where(
                        all([
                            v["x1"] > -1,
                            v["x1"] < +1,
                            isfinite(v["x1"]),
                            not(c["eb_is_zero"]),
                        ]),

                        # if $x is in bounds, scale x to fulfil the quadratic
                        # error bound, as long as eb_qua > 0:
                        #   |x - $x| <= (1 - x1^2) * eb_qua
                        #   |x - $x| / (1 - x1^2) <= eb_qua
                        #   | (x / (1 - x1^2)) - ($x / (1 - x1^2)) | <= eb_qua
                        #   |qoi(x) - qoi($x)| <= eb_qua
                        #     with qoi(x) = x / (1 - x1^2)
                        # nudge to conservatively inflate the error so that
                        #  rounding errors cannot cause a violation
                        # TODO: use operations with rounding modes instead
                        nextafter(
                            x / (1 - nextafter(
                                square(v["x1"]),
                                1
                            )),
                            Inf,
                        ),

                        # otherwise, if $x is
                        #  (a) at the bounds,
                        #  (b) out of bounds, or
                        #  (c) x could not be normalised,
                        # ensure instead that x == $x
                        where(
                            isnan(c["$x"]),

                            # use the fact that NaN results will always be
                            # preserved, and so if $x is NaN and we return x
                            # then the error bound can only be for x is NaN
                            x,

                            # use the fact that the error bound will always be
                            # finite, and so the error bound can only be met if
                            # x == $x, since this is true for $x
                            where(x == c["$x"], Inf, 0),
                        )
                    );
                    """,  # type: ignore
                    type=ErrorBound.abs,
                    eb=requirement.value,
                    early_bound=dict(
                        minimum=requirement.minimum,
                        maximum=requirement.maximum,
                        eb_is_zero=requirement.value == 0,
                    ),
                ),
            ]
        case RequirementKind.data_limits:
            assert isinstance(requirement, DataLimitsRequirement)
            safeguards: list[PointwiseSafeguard | StencilSafeguard] = []
            if requirement.minimum is not None:
                safeguards.append(
                    PointwiseQuantityOfInterestErrorBoundSafeguard(
                        qoi='x >= c["minimum"]',  # type: ignore
                        type="abs",
                        eb=0,
                        early_bound=dict(minimum=requirement.minimum),
                    )
                )
            if requirement.maximum is not None:
                safeguards.append(
                    PointwiseQuantityOfInterestErrorBoundSafeguard(
                        qoi='x <= c["maximum"]',  # type: ignore
                        type="abs",
                        eb=0,
                        early_bound=dict(maximum=requirement.maximum),
                    )
                )
            if len(safeguards) > 1:
                return [
                    AllSafeguards(  # type: ignore
                        safeguards=safeguards
                    )
                ]
            return safeguards
        case RequirementKind.isovalue:
            assert isinstance(requirement, IsovalueRequirement)
            return [SignPreservingSafeguard(offset=requirement.value)]
        case RequirementKind.missing_value:
            assert isinstance(requirement, MissingValueRequirement)
            return [EquivalentValueSafeguard(value=requirement.value, exclusive=True)]
        case RequirementKind.lossless:
            assert isinstance(requirement, LosslessRequirement)
            return [LosslessSafeguard()]
        case _:
            assert_never(requirement.kind)
