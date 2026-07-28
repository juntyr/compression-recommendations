import importlib.metadata

import compression_recommendations


def test_version():
    package_version = importlib.metadata.version("compression_recommendations")
    recommendations_version = compression_recommendations._RECOMMENDATIONS["version"].value

    assert package_version == recommendations_version
