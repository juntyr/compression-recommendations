"""
# Recommendations for Safe Lossy Compression of weather and climate data

What lossy compression is safe when using lossy compression on weather and climate data?

This package contains the [community-provided][.Recommendations.provide]
[`Recommendations`][.Recommendations], that recommend appropriate safety
[`Requirement`][.requirements.abc.Requirement]s for compressing various weather
and climate data.

```py
import compression_recommendations

compression_recommendations.Recommendations.provide.search(markers={
    "cf-short-name": "cc",     # cloud cover
    "level-kind": "pressure",
})
```

We also provide the following integrations

- [`compression-requirement-safeguards`][compression_requirement_safeguards]
  translates the recommended safety requirements into
  [compression safeguards](https://compression-safeguards.readthedocs.io) that
  can be wrapped around any compressor to guarantee that the requirements are
  fulfilled.
- [`compression-requirement-checks`][compression_requirement_checks]
  checks whether safety requirements are upheld by a lossy-decompressed
  reconstruction of the original data.
"""

__all__ = ["Recommendations"]

import importlib.resources
import sys
from collections.abc import Collection, Mapping
from dataclasses import dataclass
from typing import Self

from semver.version import Version
from typed_classproperties import classproperty
from typing_extensions import override  # MSPV 3.12

from .config import Config, Format, LiteralFormat
from .recommendation import Recommendation
from .requirements.abc import Requirement
from .typing import JSON


@dataclass(kw_only=True, slots=True)
class Recommendations(Config):
    """
    A versioned collection of [`Recommendation`][compression_recommendations.recommendation.Recommendation]s, which can be queried for the recommended safety requirements for a specific use case, e.g. variable.

    Parameters
    ----------
    recommendations : Collection[Recommendation]
        The collection of recommendations that can be queried.
    version : Version
        The [semantic version](https://semver.org) of the provided
        recommendations.
    metadata : Mapping[str, JSON]
        Arbitrary metadata about the recommendations, e.g. provenance about
        their source.
    """

    recommendations: Collection[Recommendation]
    version: Version
    metadata: Mapping[str, JSON]

    @classproperty
    def provide(cls) -> "Recommendations":
        """
        Inspect the community-provided [recommendations](../../recommendations.md).

        **What is recommended?**

        That is up to *you*, the community, to decide!

        - You can *add comments* to any recommendation to elaborate or discuss
          different requirements.
        - You can *propose edits* to any recommendation, which we accept once
          a new consensus has been reached.
        - You can *create new recommendations* for new variables or to
          specialise existing requirements for specific cases.
        - You can *merge multiple recommendations* to generalise them.
        - You can *propose new filters* to select which recommendations should
          apply, or *new kinds of requirements*.

        Please feel free to contribute to the
        [`compression-recommendations`](https://github.com/juntyr/compression-recommendations)
        GitHub repository.
        """

        CACHED_ATTR = "_cached_recommendations"
        if not hasattr(cls, CACHED_ATTR):
            with (
                importlib.resources.files(sys.modules[__name__])
                .joinpath("recommendations.yaml")
                .open() as f
            ):
                setattr(cls, CACHED_ATTR, cls.load(f))
        return getattr(cls, CACHED_ATTR)

    def search(
        self, *, markers: Mapping[str, None | bool | int | float | str]
    ) -> Collection[Requirement]:
        """
        Search for the safety [`Requirement`][compression_recommendations.requirements.abc.Requirement]s that are recommended for the given use case, identified by the `markers`.

        Parameters
        ----------
        markers : Mapping[str, None | bool | int | float | str]
            The markers that identify the use case, e.g. the variable, for which
            safeguards are produced.

            Only [`Recommendation`][...recommendation.Recommendation]s whose
            [`Filter`][...filters.abc.Filter]s match the `markers` contribute
            their [`Requirement`][...requirements.abc.Requirement]s to the
            returned collection of safety requirements.

            For example, when searching for recommended requirements for
            wind speed, all recommendations covering this variable combine
            their requirements.
            Recommendations that have more specific filters, e.g. only cover a
            specific vertical level or use case, will not contribute, unless
            the `markers` are extended to describe this more specific use case.
            In the end, the returned requirements contain all
            more-generally applicable requirements, and all
            specifically-applicable requirements.

            Many filters provide a `Filter.markers_for` static method to
            construct the markers for the use case they filter for.

        Returns
        -------
        requirements : Collection[Requirement]
            The safety requirements that are recommended to all be upheld by
            lossy compression.

        Raises
        ------
        KeyError
            if no recommendations could be found for the provided `markers`.
        """

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
        """
        Construct the recommendations from the [`JSON`][compression_recommendations.typing.JSON] configurations for its `recommendations` as well as its `version` and `metadata`.

        Parameters
        ----------
        recommendations : Collection[Mapping[str, JSON]]
            The configurations for the collection of recommendations that can
            be queried.
        version : Version
            The [semantic version](https://semver.org) of the provided
            recommendations.
        metadata : Mapping[str, JSON]
            Arbitrary metadata about the recommendations, e.g. provenance about
            their source.

        Returns
        -------
        recommendations : Self
            The instantiated recommendations.
        """

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
        """
        Get the configuration of these recommendations.

        Returns
        -------
        config : Mapping[str, JSON]
            Configuration in JSON object format.
        """

        return dict(
            recommendations=[
                recommendation.get_config() for recommendation in self.recommendations
            ],
            version=str(self.version),
            metadata=self.metadata,
        )

    @override
    def humanise(self, *, format: Format | LiteralFormat = Format.plain) -> str:
        """
        Humanise the representation of these recommendations.

        Parameters
        ----------
        format : Format | LiteralFormat
            The format of the humanised representation.

        Returns
        -------
        humanised : str
            The humanised representation of these recommendations.
        """

        joiner = "\n\nand\n\n"
        return f"{joiner.join(recommendation.humanise(format=format) for recommendation in self.recommendations)}"
