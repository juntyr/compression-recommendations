"""
# Recommendations for Safe Lossy Compression of weather and climate data

```py
assert 2 + 2 == 4
```
"""

__all__ = []

import importlib.resources
import sys

import strictyaml

_RECOMMENDATIONS: strictyaml.YAML = strictyaml.load(importlib.resources.files(
    sys.modules[__name__]
).joinpath("recommendations.yaml").read_text())
