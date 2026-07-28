"""
# Recommendations for Safe Lossy Compression of weather and climate data

```py
assert 2 + 2 == 4
```
"""

__all__ = ["RECOMMENDATIONS"]

import importlib.resources
import sys

import strictyaml

from .typing import JSON, _parse_yaml

RECOMMENDATIONS: JSON = _parse_yaml(
    strictyaml.load(
        importlib.resources.files(sys.modules[__name__])
        .joinpath("recommendations.yaml")
        .read_text()
    )
)
