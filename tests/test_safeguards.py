import compression_safeguards_recommendations
import pytest
from compression_safeguards.api import Safeguards
from compression_safeguards.safeguards.combinators.all import AllSafeguards
from compression_safeguards.safeguards.combinators.any import AnySafeguard
from compression_safeguards.safeguards.pointwise.eb import ErrorBoundSafeguard

from compression_recommendations import Recommendations
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
from compression_recommendations.requirements.limits import DataLimitsRequirement
from compression_recommendations.requirements.missing import MissingValueRequirement


def test_recommended_safeguards_for_u10():
    assert (
        compression_safeguards_recommendations.recommended_safeguards_for(
            markers={"cf-short-name": "u10", "level-kind": "single"}
        ).get_config()
        == Safeguards(
            safeguards=[
                AnySafeguard(
                    safeguards=[
                        AllSafeguards(
                            safeguards=[
                                ErrorBoundSafeguard(type="abs", eb=0.5, equal_nan=False)
                            ]
                        ),
                        AllSafeguards(
                            safeguards=[
                                ErrorBoundSafeguard(type="rel", eb=0.5, equal_nan=False)
                            ]
                        ),
                    ]
                ),
            ]
        ).get_config()
    )


def test_all_recommendations():
    for recommendation in Recommendations.provide.recommendations:
        for requirement in recommendation.requirements:
            compression_safeguards_recommendations.safeguards_for_requirement(
                requirement
            )


@pytest.mark.parametrize("cls", [AnyRequirement, AllRequirements])
def test_combinator_requirement(cls):
    with pytest.raises(
        ValueError, match="can only combine over at least one safeguard"
    ):
        compression_safeguards_recommendations.safeguards_for_requirement(
            cls(requirements=[])
        )

    compression_safeguards_recommendations.safeguards_for_requirement(
        cls(requirements=[IsovalueRequirement(value=0)])
    )

    compression_safeguards_recommendations.safeguards_for_requirement(
        cls(requirements=[IsovalueRequirement(value=0), IsovalueRequirement(value=1)])
    )


@pytest.mark.parametrize(
    "cls",
    [
        MaxPointwiseAbsoluteErrorBoundRequirement,
        MaxPointwiseRelativeErrorBoundRequirement,
        MaxPointwiseRangeRelativeErrorBoundRequirement,
        MeanAbsoluteErrorBoundRequirement,
        MeanRelativeErrorBoundRequirement,
        MeanRangeRelativeErrorBoundRequirement,
    ],
)
def test_error_bound_requirement(cls):
    compression_safeguards_recommendations.safeguards_for_requirement(cls(value=4.2))


def test_quadrartic_error_bound_requirement():
    compression_safeguards_recommendations.safeguards_for_requirement(
        MaxPointwiseQuadraticErrorBoundRequirement(value=4.2, minimum=-10, maximum=10)
    )


def test_data_limits_requirement():
    assert (
        len(
            compression_safeguards_recommendations.safeguards_for_requirement(
                DataLimitsRequirement()
            )
        )
        == 0
    )
    assert (
        len(
            compression_safeguards_recommendations.safeguards_for_requirement(
                DataLimitsRequirement(minimum=-10)
            )
        )
        == 1
    )
    assert (
        len(
            compression_safeguards_recommendations.safeguards_for_requirement(
                DataLimitsRequirement(maximum=10)
            )
        )
        == 1
    )
    assert (
        len(
            compression_safeguards_recommendations.safeguards_for_requirement(
                DataLimitsRequirement(minimum=-10, maximum=10)
            )
        )
        == 2
    )


def test_isovalue_requirement():
    compression_safeguards_recommendations.safeguards_for_requirement(
        IsovalueRequirement(value=4.2)
    )


def test_missing_value_requirement():
    compression_safeguards_recommendations.safeguards_for_requirement(
        MissingValueRequirement(value=99999)
    )
    compression_safeguards_recommendations.safeguards_for_requirement(
        MissingValueRequirement(value=-0.0)
    )
    compression_safeguards_recommendations.safeguards_for_requirement(
        MissingValueRequirement(value=float("nan"))
    )
