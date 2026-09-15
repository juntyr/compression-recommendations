import importlib.metadata
from pathlib import Path

import strictyaml
from packaging.version import Version as PyPIVersion
from semver import Version

import compression_recommendations


def test_version():
    package_version = importlib.metadata.version("compression_recommendations")
    recommendations_version = (
        compression_recommendations.Recommendations.provide.version
    )

    # based on https://python-semver.readthedocs.io/en/latest/advanced/convert-pypi-to-semver.html#from-pypi-to-semver
    pyversion = PyPIVersion(package_version)
    pre = None if not pyversion.pre else "".join([str(i) for i in pyversion.pre])
    version = Version(*pyversion.release, prerelease=pre, build=pyversion.dev)

    assert version == recommendations_version


def test_search():
    recs = compression_recommendations.Recommendations.provide

    single_u10_reqs = compression_recommendations.Recommendation.from_config(
        **compression_recommendations.config._parse_yaml(
            strictyaml.load(
                Path("recommendations").joinpath("single-u10.yaml").read_text()
            )
        )
    ).requirements

    assert (
        recs.search(markers={"cf-short-name": "u10", "level-kind": "single"})
        == single_u10_reqs
    )
