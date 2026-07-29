import importlib.metadata
from pathlib import Path

import strictyaml
from semver import Version

import compression_recommendations


def test_version():
    package_version = importlib.metadata.version("compression_recommendations")
    recommendations_version = (
        compression_recommendations.Recommendations.provide.version
    )

    assert Version.parse(package_version) == recommendations_version


def test_search():
    recs = compression_recommendations.Recommendations.provide

    single_u10_reqs = compression_recommendations.Recommendation.from_config(
        **compression_recommendations.typing._parse_yaml(
            strictyaml.load(
                Path("recommendations").joinpath("single-u10.yaml").read_text()
            )
        )
    ).requirements

    assert (
        recs.search(markers={"cf-short-name": "u10", "level-kind": "single"})
        == single_u10_reqs
    )
