"""
Implementation of a single [`Recommendation`][compression_recommendations.recommendation.Recommendation].
"""

from collections.abc import Collection, Mapping
from dataclasses import dataclass
from typing import Self

from typing_extensions import override  # MSPV 3.12

from .config import Config, Format, LiteralFormat
from .filters.abc import Filter
from .requirements.abc import Requirement
from .typing import JSON


@dataclass(kw_only=True, slots=True)
class Recommendation(Config):
    """
    A recommendation for safe lossy compression for a specific use case.

    Each recommendation connects a set of [`Filter`][...filters.abc.Filter]s to
    a set of safety [`Requirement`][...requirements.abc.Requirement]s.

    For example, an error bound can be applied to one or more variables,
    possibly limited to a specific vertical level range or a specific
    downstream application.

    Parameters
    ----------
    filters : Collection[Filter]
        The collection of filters that decide when the recommendation applies.
        All filters must [`match`][...filters.abc.Filter.matches] for the
        recommendation to apply.

        Please refer to the [`FilterKind`][...filters.kind.FilterKind] for an
        enumeration of all supported filters.
    requirements : Collection[Requirement]
        The collection of safety requirements that are recommended to all be
        upheld by lossy compression.

        Please refer to the
        [`RequirementKind`][...requirements.kind.RequirementKind] for an
        enumeration of all supported requirements.
    """

    filters: Collection[Filter]
    requirements: Collection[Requirement]

    def matches(
        self, *, markers: Mapping[str, None | bool | int | float | str]
    ) -> bool:
        """
        Check if the `markers` match this recommendation.

        All filters must [`match`][....filters.abc.Filter.matches] for the
        recommendation to apply.

        Parameters
        ----------
        markers : Mapping[str, None | bool | int | float | str]
            The markers that identify the use case, e.g. the variable.

        Returns
        -------
        matches : bool
            [`True`][True] if the `markers` match, [`False`][False] otherwise.
        """

        all_match = True

        for filter in self.filters:
            all_match &= filter.matches(markers=markers)

        return all_match

    @override
    @classmethod
    def from_config(  # type: ignore
        cls,
        *,
        filters: Collection[Mapping[str, JSON]],
        requirements: Collection[Mapping[str, JSON]],
    ) -> Self:
        """
        Construct the recommendation from the [`JSON`][compression_recommendations.typing.JSON] configurations for its `filters` and `requirements`.

        Parameters
        ----------
        filters : Collection[Mapping[str, JSON]]
            The configurations for the collection of filters that decide when
            the recommendation applies.
        requirements : Collection[Mapping[str, JSON]]
            The configurations for the collection of safety requirements that
            are recommended to all be upheld by lossy compression.

        Returns
        -------
        filter : Self
            The instantiated recommendation.
        """

        return cls(
            filters=tuple(
                Filter.from_config(
                    **filter  # type: ignore
                )
                for filter in filters
            ),
            requirements=tuple(
                Requirement.from_config(
                    **requirement  # type: ignore
                )
                for requirement in requirements
            ),
        )

    @override
    def get_config(self) -> Mapping[str, JSON]:
        """
        Get the configuration of this recommendation.

        Returns
        -------
        config : Mapping[str, JSON]
            Configuration in JSON object format.
        """

        return dict(
            filters=[filter.get_config() for filter in self.filters],
            requirements=[
                requirement.get_config() for requirement in self.requirements
            ],
        )

    @override
    def humanise(self, *, format: Format | LiteralFormat = Format.plain) -> str:
        """
        Humanise the representation of this recommendation.

        Parameters
        ----------
        format : Format | LiteralFormat
            The format of the humanised representation.

        Returns
        -------
        humanised : str
            The humanised representation of this recommendation.
        """

        from .filters.combinators import AllFilters  # noqa: PLC0415
        from .requirements.combinators import AllRequirements  # noqa: PLC0415

        humanised_filters = AllFilters(filters=self.filters).humanise(format=format)
        humanised_requirements = AllRequirements(
            requirements=self.requirements
        ).humanise(format=format)

        return f"{humanised_filters} -> {humanised_requirements}"
