"""
Logical combinations of multiple filters.
"""

from collections.abc import Collection, Mapping
from dataclasses import dataclass
from typing import ClassVar, Self

from typing_extensions import override  # MSPV 3.12

from ..config import Format, LiteralFormat, _humanise_labelled_type
from ..typing import JSON
from .abc import Filter
from .kind import FilterKind

__all__ = ["AnyFilter", "AllFilters"]


@dataclass(kw_only=True, slots=True)
class AnyFilter(Filter):
    """
    Filter that matches if at least one of the provided sub-`filters` matches.

    Parameters
    ----------
    filters : Collection[Filter]
        The sub-filters for this any-filter combinator.
    """

    kind: ClassVar[FilterKind] = FilterKind.any
    filters: Collection[Filter]

    def matches(
        self, *, markers: Mapping[str, None | bool | int | float | str]
    ) -> bool:
        """
        Check if the `markers` match at least one of the sub-filters of this any-filter combinator.

        Parameters
        ----------
        markers : Mapping[str, None | bool | int | float | str]
            The markers to check.

        Returns
        -------
        matches : bool
            [`True`][True] if the `markers` match, [`False`][False] otherwise.
        """

        any_match = False

        for filter in self.filters:
            any_match |= filter.matches(markers=markers)

        return any_match

    @override
    @classmethod
    def from_config(  # type: ignore
        cls,
        *,
        filters: Collection[Mapping[str, JSON]],
    ) -> Self:
        """
        Construct the any-filter combinator from its configuration.

        Parameters
        ----------
        filters : Collection[Filter]
            The sub-filters for this any-filter combinator.

        Returns
        -------
        filter : Self
            The instantiated any-filter combinator.
        """

        return cls(
            filters=tuple(
                Filter.from_config(
                    **filter  # type: ignore
                )
                for filter in filters
            )
        )

    @override
    def get_config(self) -> Mapping[str, JSON]:
        """
        Get the configuration of this any-filter combinator.

        Returns
        -------
        config : Mapping[str, JSON]
            Configuration in JSON object format.
        """

        return dict(
            kind=type(self).kind.get_config(),
            filters=[filter.get_config() for filter in self.filters],
        )

    @override
    def humanise(self, *, format: Format | LiteralFormat = Format.plain) -> str:
        """
        Humanise the representation of this any-filter combinator.

        Parameters
        ----------
        format : Format | LiteralFormat
            The format of the humanised representation.

        Returns
        -------
        humanised : str
            The humanised representation of this any-filter combinator.
        """

        match self.filters:
            case ():
                return _humanise_labelled_type(self, label="False", format=format)
            case (filter,):
                return filter.humanise(format=format)
            case filters:
                or_ = _humanise_labelled_type(self, label="or", format=format)
                return f"({f' {or_} '.join(filter.humanise(format=format) for filter in filters)})"


@dataclass(kw_only=True, slots=True)
class AllFilters(Filter):
    """
    Filter that matches if all of the provided sub-`filters` matches.

    Parameters
    ----------
    filters : Collection[Filter]
        The sub-filters for this all-filters combinator.
    """

    kind: ClassVar[FilterKind] = FilterKind.all
    filters: Collection[Filter]

    def matches(
        self, *, markers: Mapping[str, None | bool | int | float | str]
    ) -> bool:
        """
        Check if the `markers` match all of the sub-filters of this all-filters combinator.

        Parameters
        ----------
        markers : Mapping[str, None | bool | int | float | str]
            The markers to check.

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
    ) -> Self:
        """
        Construct the all-filters combinator from its configuration.

        Parameters
        ----------
        filters : Collection[Filter]
            The sub-filters for this all-filters combinator.

        Returns
        -------
        filter : Self
            The instantiated all-filters combinator.
        """

        return cls(
            filters=tuple(
                Filter.from_config(
                    **filter  # type: ignore
                )
                for filter in filters
            )
        )

    @override
    def get_config(self) -> Mapping[str, JSON]:
        """
        Get the configuration of this all-filters combinator.

        Returns
        -------
        config : Mapping[str, JSON]
            Configuration in JSON object format.
        """

        return dict(
            kind=type(self).kind.get_config(),
            filters=[filter.get_config() for filter in self.filters],
        )

    @override
    def humanise(self, *, format: Format | LiteralFormat = Format.plain) -> str:
        """
        Humanise the representation of this all-filters combinator.

        Parameters
        ----------
        format : Format | LiteralFormat
            The format of the humanised representation.

        Returns
        -------
        humanised : str
            The humanised representation of this all-filters combinator.
        """

        match self.filters:
            case ():
                return _humanise_labelled_type(self, label="True", format=format)
            case (filter,):
                return filter.humanise(format=format)
            case filters:
                and_ = _humanise_labelled_type(self, label="and", format=format)
                return f"({f' {and_} '.join(filter.humanise(format=format) for filter in filters)})"
