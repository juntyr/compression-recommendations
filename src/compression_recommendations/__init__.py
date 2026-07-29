"""
# Recommendations for Safe Lossy Compression of weather and climate data

```py
assert 2 + 2 == 4
```
"""

__all__ = ["Recommendations"]

import importlib.resources
import sys
from collections.abc import Collection, Mapping
from dataclasses import dataclass
from functools import cache
from typing import Self, override

import strictyaml
from semver import Version
from typed_classproperties import classproperty

from .config import Config
from .recommendation import Recommendation
from .requirements.abc import Requirement
from .typing import JSON, _parse_yaml


@dataclass(kw_only=True)
class Recommendations(Config):
    recommendations: Collection[Recommendation]
    version: Version
    metadata: Mapping[str, JSON]

    @classproperty
    @cache
    def provide(cls) -> Self:
        return Recommendations.from_config(
            **_parse_yaml(  # type: ignore
                strictyaml.load(
                    importlib.resources.files(sys.modules[__name__])
                    .joinpath("recommendations.yaml")
                    .read_text()
                )
            )
        )

    def search(
        self, *, markers: Mapping[str, None | bool | int | float | str]
    ) -> Collection[Requirement]:
        any_match = False
        requirements: list[Requirement] = []

        for recommendation in self.recommendations:
            if recommendation.matches(markers=markers):
                any_match = True
                requirements.extend(recommendation.requirements)

        if any_match:
            return tuple(requirements)

        raise KeyError("failed to find a matching recommendation", markers)

    @override
    @classmethod
    def from_config(  # type: ignore
        cls,
        *,
        recommendations: Collection[Mapping[str, JSON]],
        version: str,
        metadata: Mapping[str, JSON],
    ) -> Self:
        return cls(
            recommendations=tuple(
                Recommendation.from_config(
                    **recommendation  # type: ignore
                )
                for recommendation in recommendations
            ),
            version=Version.parse(version),
            metadata=metadata,
        )

    @override
    def get_config(self) -> JSON:
        return dict(
            recommendations=tuple(
                recommendation.get_config() for recommendation in self.recommendations
            ),
            version=str(self.version),
            metadata=self.metadata,
        )
