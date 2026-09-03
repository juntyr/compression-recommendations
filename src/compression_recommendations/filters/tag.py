"""
Filters for arbitrary tags.
"""

from collections.abc import Mapping
from dataclasses import dataclass
from typing import ClassVar, Self

from typing_extensions import override  # MSPV 3.12

from ..config import Format, LiteralFormat, _humanise_kinded_type
from ..typing import JSON
from .abc import Filter
from .kind import FilterKind

__all__ = ["TagFilter"]


@dataclass(kw_only=True, slots=True)
class TagFilter(Filter):
    """
    Filter that matches on the given arbitrary tag.

    Parameters
    ----------
    value : str
        The arbitrary tag to match.
    """

    kind: ClassVar[FilterKind] = FilterKind.tag
    value: str

    def matches(
        self, *, markers: Mapping[str, None | bool | int | float | str]
    ) -> bool:
        """
        Check if the `markers` contain this filter's tag.

        Parameters
        ----------
        markers : Mapping[str, None | bool | int | float | str]
            The markers to check.

        Returns
        -------
        matches : bool
            [`True`][True] if the `markers` match, [`False`][False] otherwise.
        """

        if "tags" not in markers:
            return False
        tags = markers["tags"]
        if not isinstance(tags, str):
            return False
        return self.value in tags.split(",")

    @classmethod
    def markers_for(cls, *values: str) -> Mapping[str, None | bool | int | float | str]:
        """
        Construct the markers that can be passed to
        [`Recommendations.search`][.....Recommendations.search] or
        [`Filter.matches`][....abc.Filter.matches]
        to find recommendations for the given tags.

        Parameters
        ----------
        *values : str
            The tags to match.

        Returns
        -------
        marker : Mapping[str, None | bool | int | float | str]
            The markers that will match any of the given tags.
        """

        return {"tags": ",".join(values)}

    @override
    @classmethod
    def from_config(  # type: ignore
        cls,
        *,
        value: str,
    ) -> Self:
        """
        Construct the tag filter from its configuration.

        Parameters
        ----------
        value : str
            The arbitrary tag to match.

        Returns
        -------
        filter : Self
            The instantiated tag filter.
        """

        return cls(value=value)

    @override
    def get_config(self) -> Mapping[str, JSON]:
        """
        Get the configuration of this tag filter.

        Returns
        -------
        config : Mapping[str, JSON]
            Configuration in JSON object format.
        """

        return dict(kind=type(self).kind.get_config(), value=self.value)

    @override
    def humanise(self, *, format: Format | LiteralFormat = Format.plain) -> str:
        """
        Humanise the representation of this tag filter.

        Parameters
        ----------
        format : Format | LiteralFormat
            The format of the humanised representation.

        Returns
        -------
        humanised : str
            The humanised representation of this tag filter.
        """

        return f"{_humanise_kinded_type(self, format=format)}({self.value})"
