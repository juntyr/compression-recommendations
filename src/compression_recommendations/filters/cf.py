"""
Filters for CF metadata attributes.
"""

from collections.abc import Mapping
from dataclasses import dataclass
from typing import ClassVar, Self

from typing_extensions import override  # MSPV 3.12

from ..config import Format, LiteralFormat, _humanise_kinded_type
from ..typing import JSON
from .abc import Filter
from .kind import FilterKind

__all__ = ["CfStandardNameFilter", "CfShortNameFilter"]


@dataclass(kw_only=True, slots=True)
class CfStandardNameFilter(Filter):
    """
    Filter that matches on the [CF Standard Name](https://cfconventions.org/Data/cf-standard-names/current/build/cf-standard-name-table.html) of a variable.

    Parameters
    ----------
    value : str
        The CF Standard Name to match.
    """

    kind: ClassVar[FilterKind] = FilterKind.cf_standard_name
    value: str

    def matches(
        self, *, markers: Mapping[str, None | bool | int | float | str]
    ) -> bool:
        """
        Check if the `markers` match this filter's CF Standard Name.

        Parameters
        ----------
        markers : Mapping[str, None | bool | int | float | str]
            The markers to check.

        Returns
        -------
        matches : bool
            [`True`][True] if the `markers` match, [`False`][False] otherwise.
        """

        if type(self).kind.value not in markers:
            return False
        return markers[type(self).kind.value] == self.value

    @classmethod
    def markers_for(cls, value: str) -> Mapping[str, None | bool | int | float | str]:
        """
        Construct the markers that can be passed to
        [`Recommendations.search`][.....Recommendations.search] or
        [`Filter.matches`][....abc.Filter.matches]
        to find recommendations for the given CF Standard Name.

        Parameters
        ----------
        value : str
            The CF Standard Name to match.

        Returns
        -------
        marker : Mapping[str, None | bool | int | float | str]
            The markers that will match the given CF Standard Name.
        """

        return {cls.kind.value: value}

    @override
    @classmethod
    def from_config(  # type: ignore
        cls,
        *,
        value: str,
    ) -> Self:
        """
        Construct the CF Standard Name filter from its configuration.

        Parameters
        ----------
        value : str
            The CF Standard Name to match.

        Returns
        -------
        filter : Self
            The instantiated CF Standard Name filter.
        """

        return cls(value=value)

    @override
    def get_config(self) -> Mapping[str, JSON]:
        """
        Get the configuration of this CF Standard Name filter.

        Returns
        -------
        config : Mapping[str, JSON]
            Configuration in JSON object format.
        """

        return dict(kind=type(self).kind.get_config(), value=self.value)

    @override
    def humanise(self, *, format: Format | LiteralFormat = Format.plain) -> str:
        """
        Humanise the representation of this CF Standard Name filter.

        Parameters
        ----------
        format : Format | LiteralFormat
            The format of the humanised representation.

        Returns
        -------
        humanised : str
            The humanised representation of this CF Standard Name filter.
        """

        return f"{_humanise_kinded_type(self, format=format)}({self.value})"


@dataclass(kw_only=True, slots=True)
class CfShortNameFilter(Filter):
    """
    Filter that matches on the non-standard CF short name of a variable.

    Parameters
    ----------
    value : str
        The non-standard CF short name to match.
    """

    kind: ClassVar[FilterKind] = FilterKind.cf_short_name
    value: str

    def matches(
        self, *, markers: Mapping[str, None | bool | int | float | str]
    ) -> bool:
        """
        Check if the `markers` match this filter's non-standard CF short name.

        Parameters
        ----------
        markers : Mapping[str, None | bool | int | float | str]
            The markers to check.

        Returns
        -------
        matches : bool
            [`True`][True] if the `markers` match, [`False`][False] otherwise.
        """

        if type(self).kind.value not in markers:
            return False
        return markers[type(self).kind.value] == self.value

    @classmethod
    def markers_for(cls, value: str) -> Mapping[str, None | bool | int | float | str]:
        """
        Construct the markers that can be passed to
        [`Recommendations.search`][.....Recommendations.search] or
        [`Filter.matches`][....abc.Filter.matches]
        to find recommendations for the given non-standard CF short name.

        Parameters
        ----------
        value : str
            The CF short name to match.

        Returns
        -------
        marker : Mapping[str, None | bool | int | float | str]
            The markers that will match the given CF short name.
        """

        return {cls.kind.value: value}

    @override
    @classmethod
    def from_config(  # type: ignore
        cls,
        *,
        value: str,
    ) -> Self:
        """
        Construct the CF short name filter from its configuration.

        Parameters
        ----------
        value : str
            The non-standard CF short name to match.

        Returns
        -------
        filter : Self
            The instantiated CF short name filter.
        """

        return cls(value=value)

    @override
    def get_config(self) -> Mapping[str, JSON]:
        """
        Get the configuration of this CF short name filter.

        Returns
        -------
        config : Mapping[str, JSON]
            Configuration in JSON object format.
        """

        return dict(kind=type(self).kind.get_config(), value=self.value)

    @override
    def humanise(self, *, format: Format | LiteralFormat = Format.plain) -> str:
        """
        Humanise the representation of this CF short name filter.

        Parameters
        ----------
        format : Format | LiteralFormat
            The format of the humanised representation.

        Returns
        -------
        humanised : str
            The humanised representation of this CF short name filter.
        """

        return f"{_humanise_kinded_type(self, format=format)}({self.value})"
