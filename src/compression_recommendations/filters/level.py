"""
Filters for vertical levels.
"""

from collections.abc import Mapping
from dataclasses import dataclass
from enum import StrEnum
from typing import ClassVar, Self, assert_never

from typing_extensions import override  # MSPV 3.12

from ..config import (
    Format,
    LiteralFormat,
    _humanise_kinded_type,
    _humanise_labelled_type,
    _parse_number,
)
from ..typing import JSON
from .abc import Filter
from .kind import FilterKind

__all__ = ["LevelKind", "LevelKindFilter", "LevelValueFilter"]


class LevelKind(StrEnum):
    """
    Enumeration of the vertical level kinds.
    """

    single = "single"
    """ Single-level 2D data represents conditions at the Earth's surface, specific near-surface heights, or vertical integrals across all vertical levels. """

    pressure = "pressure"
    """ Pressure-level data represents conditions at one (2D) or more (3D) specific atmospheric pressure levels. """

    @classmethod
    def from_config(  # type: ignore
        cls, *, kind: str
    ) -> Self:
        """
        Construct the level kind from its configuration.

        Parameters
        ----------
        kind : str
            The level kind name.

        Returns
        -------
        kind : Self
            The instantiated level kind.
        """

        return cls[kind.replace("-", "_")]

    def get_config(self) -> JSON:
        """
        Get the configuration of this level kind.

        Returns
        -------
        config : JSIN
            Configuration in JSON format.
        """

        return self.value

    def humanise(self, *, format: Format | LiteralFormat = Format.plain) -> str:
        """
        Humanise the representation of this level kind.

        Parameters
        ----------
        format : Format | LiteralFormat
            The format of the humanised representation.

        Returns
        -------
        humanised : str
            The humanised representation of this level kind.
        """

        return _humanise_labelled_type(self, label=self.value, format=format)


@dataclass(kw_only=True, slots=True)
class LevelKindFilter(Filter):
    """
    Filter that matches on the kind of vertical level of the data.

    Parameters
    ----------
    value : LevelKind
        The level kind to match.
    """

    kind: ClassVar[FilterKind] = FilterKind.level_kind
    value: LevelKind

    def matches(
        self, *, markers: Mapping[str, None | bool | int | float | str]
    ) -> bool:
        """
        Check if the `markers` match this filter's level kind.

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
        return markers[type(self).kind.value] == self.value.value

    @classmethod
    def markers_for(
        cls, value: LevelKind
    ) -> Mapping[str, None | bool | int | float | str]:
        """
        Construct the markers to find recommendations for the given level kind.

        The markers can be passed to
        [`Recommendations.search`][.....Recommendations.search] or
        [`Filter.matches`][....abc.Filter.matches].

        Parameters
        ----------
        value : LevelKind
            The level kind to match.

        Returns
        -------
        marker : Mapping[str, None | bool | int | float | str]
            The markers that will match the given level kind.
        """

        return {cls.kind.value: value.value}

    @override
    @classmethod
    def from_config(  # type: ignore
        cls,
        *,
        value: str,
    ) -> Self:
        """
        Construct the level kind filter from its configuration.

        Parameters
        ----------
        value : str
            The level kind to match.

        Returns
        -------
        filter : Self
            The instantiated level kind filter.
        """

        return cls(value=LevelKind.from_config(kind=value))

    @override
    def get_config(self) -> Mapping[str, JSON]:
        """
        Get the configuration of this level kind filter.

        Returns
        -------
        config : Mapping[str, JSON]
            Configuration in JSON object format.
        """

        return dict(kind=type(self).kind.get_config(), value=self.value.get_config())

    @override
    def humanise(self, *, format: Format | LiteralFormat = Format.plain) -> str:
        """
        Humanise the representation of this level kind filter.

        Parameters
        ----------
        format : Format | LiteralFormat
            The format of the humanised representation.

        Returns
        -------
        humanised : str
            The humanised representation of this level kind filter.
        """

        return f"{_humanise_kinded_type(self, format=format)}({self.value.humanise(format=format)})"


@dataclass(kw_only=True, slots=True)
class LevelValueFilter(Filter):
    """
    Filter that matches within a range of vertical level values of the data.

    If no `minimum` and no `maximum` are given, all vertical level values
    match.

    Parameters
    ----------
    minimum : None | int | float
        The optional inclusive minimum of the range of vertical levels that
        match.

        If no `minimum` is given, all level values below and inclusive the
        `maximum` match.
    maximum : None | int | float
        The optional inclusive maximum of the range of vertical levels that
        match.

        If no `maximum` is given, all level values above and inclusive the
        `minimum` match.
    """

    kind: ClassVar[FilterKind] = FilterKind.level_value
    minimum: None | int | float = None
    maximum: None | int | float = None

    def matches(
        self, *, markers: Mapping[str, None | bool | int | float | str]
    ) -> bool:
        """
        Check if the `markers` match within this filter's level value range.

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
        level = markers[type(self).kind.value]
        if not isinstance(level, int | float):
            return False
        if self.minimum is not None and level < self.minimum:
            return False
        if self.maximum is not None and level > self.maximum:
            return False
        return True

    @classmethod
    def markers_for(
        cls, value: int | float
    ) -> Mapping[str, None | bool | int | float | str]:
        """
        Construct the markers to find recommendations for the given vertical level value.

        The markers can be passed to
        [`Recommendations.search`][.....Recommendations.search] or
        [`Filter.matches`][....abc.Filter.matches].

        Parameters
        ----------
        value : int | float
            The vertical level value to match.

        Returns
        -------
        marker : Mapping[str, None | bool | int | float | str]
            The markers that will match the given vertical level value.
        """

        return {cls.kind.value: value}

    @override
    @classmethod
    def from_config(  # type: ignore
        cls,
        *,
        minimum: None | int | float = None,
        maximum: None | int | float = None,
    ) -> Self:
        """
        Construct the level value filter from its configuration.

        Parameters
        ----------
        minimum : None | int | float
            The optional inclusive minimum of the range of vertical levels that
            match.

            If no `minimum` is given, all level values below and inclusive the
            `maximum` match.
        maximum : None | int | float
            The optional inclusive maximum of the range of vertical levels that
            match.

            If no `maximum` is given, all level values above and inclusive the
            `minimum` match.

        Returns
        -------
        filter : Self
            The instantiated level value filter.
        """

        return cls(
            minimum=None if minimum is None else _parse_number(minimum),
            maximum=None if maximum is None else _parse_number(maximum),
        )

    @override
    def get_config(self) -> Mapping[str, JSON]:
        """
        Get the configuration of this level value filter.

        Returns
        -------
        config : Mapping[str, JSON]
            Configuration in JSON object format.
        """

        config: dict[str, JSON] = dict(kind=type(self).kind.get_config())
        if self.minimum is not None:
            config["minimum"] = self.minimum
        if self.maximum is not None:
            config["maximum"] = self.maximum
        return config

    @override
    def humanise(self, *, format: Format | LiteralFormat = Format.plain) -> str:
        """
        Humanise the representation of this level value filter.

        Parameters
        ----------
        format : Format | LiteralFormat
            The format of the humanised representation.

        Returns
        -------
        humanised : str
            The humanised representation of this level value filter.
        """

        ty = _humanise_kinded_type(self, format=format)
        limits = (self.minimum, self.maximum)
        match limits:
            case (None, None):
                return f"{ty}()"
            case (minimum, None):
                return f"{ty}(minimum={minimum})"
            case (None, maximum):
                return f"{ty}(maximum={maximum})"
            case (minimum, maximum):
                return f"{ty}(minimum={minimum}, maximum={maximum})"
            case _:
                assert_never(limits)
