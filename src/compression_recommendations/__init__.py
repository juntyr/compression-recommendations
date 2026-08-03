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
from typing import Self

from semver.version import Version
from typed_classproperties import classproperty
from typing_extensions import override  # MSPV 3.12

from .config import Config
from .recommendation import Recommendation
from .requirements.abc import Requirement
from .typing import JSON


@dataclass(kw_only=True, slots=True)
class Recommendations(Config):
    recommendations: Collection[Recommendation]
    version: Version
    metadata: Mapping[str, JSON]

    @classproperty
    @cache
    def provide(cls) -> Self:
        with (
            importlib.resources.files(sys.modules[__name__])
            .joinpath("recommendations.yaml")
            .open() as f
        ):
            return cls.load(f)

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
    def get_config(self) -> Mapping[str, JSON]:
        return dict(
            recommendations=[
                recommendation.get_config() for recommendation in self.recommendations
            ],
            version=str(self.version),
            metadata=self.metadata,
        )
