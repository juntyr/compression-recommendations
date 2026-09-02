"""
Filters for CF metadata attributes.
"""

from collections.abc import Mapping
from dataclasses import dataclass
from typing import ClassVar, Literal, Self

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
        kind: Literal["cf-standard-name"] = FilterKind.cf_standard_name.value,
    ) -> Self:
        return cls(value=value)

    @override
    def get_config(self) -> Mapping[str, JSON]:
        return dict(kind=type(self).kind.get_config(), value=self.value)

    @override
    def humanise(self, *, format: Format | LiteralFormat = Format.plain) -> str:
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
        kind: Literal["cf-short-name"] = FilterKind.cf_short_name.value,
    ) -> Self:
        return cls(value=value)

    @override
    def get_config(self) -> Mapping[str, JSON]:
        return dict(kind=type(self).kind.get_config(), value=self.value)

    @override
    def humanise(self, *, format: Format | LiteralFormat = Format.plain) -> str:
        return f"{_humanise_kinded_type(self, format=format)}({self.value})"
