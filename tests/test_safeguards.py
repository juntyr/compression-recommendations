import compression_safeguards_recommendations
from compression_safeguards.api import Safeguards
from compression_safeguards.safeguards.combinators.all import AllSafeguards
from compression_safeguards.safeguards.combinators.any import AnySafeguard
from compression_safeguards.safeguards.pointwise.eb import ErrorBoundSafeguard


def test_requirements():
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
                                ErrorBoundSafeguard(type="abs", eb=0.5, equal_nan=False)
                            ]
                        ),
                    ]
                ),
            ]
        ).get_config()
    )
