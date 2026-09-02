"""
Filters for vertical levels.
"""

from collections.abc import Mapping
from dataclasses import dataclass
from enum import StrEnum
from typing import ClassVar, Literal, Self, assert_never

from typing_extensions import override  # MSPV 3.12

from ..config import Format, LiteralFormat, _humanise_kinded_type, _parse_number
from ..typing import JSON
from .abc import Filter
from .kind import FilterKind

__all__ = ["LevelKind", "LevelKindFilter", "LevelValueFilter"]


class LevelKind(StrEnum):
    single = "single"
    pressure = "pressure"

    @classmethod
    def from_config(  # type: ignore
        cls, kind: Literal["single"] | Literal["pressure"]
    ) -> Self:
        return cls[kind.replace("-", "_")]

    def get_config(self) -> JSON:
        return self.value

    def humanise(self) -> str:
        return self.value


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
        if type(self).kind.value not in markers:
            return False
        return markers[type(self).kind.value] == self.value.value

    @classmethod
    def markers_for(
        cls, value: LevelKind
    ) -> Mapping[str, None | bool | int | float | str]:
        """
        Construct the markers that can be passed to
        [`Recommendations.search`][.....Recommendations.search] or
        [`Filter.matches`][....abc.Filter.matches]
        to find recommendations for the given level kind.

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
        value: Literal["single"] | Literal["pressure"],
        kind: Literal["level-kind"] = FilterKind.level_kind.value,
    ) -> Self:
        return cls(value=LevelKind.from_config(value))

    @override
    def get_config(self) -> Mapping[str, JSON]:
        return dict(kind=type(self).kind.get_config(), value=self.value.get_config())

    @override
    def humanise(self, *, format: Format | LiteralFormat = Format.plain) -> str:
        return f"{_humanise_kinded_type(self, format=format)}({self.value.humanise()})"


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
        Construct the markers that can be passed to
        [`Recommendations.search`][.....Recommendations.search] or
        [`Filter.matches`][....abc.Filter.matches]
        to find recommendations for the given vertical level value.

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
        kind: Literal["level-value"] = FilterKind.level_value.value,
    ) -> Self:
        return cls(
            minimum=None if minimum is None else _parse_number(minimum),
            maximum=None if maximum is None else _parse_number(maximum),
        )

    @override
    def get_config(self) -> Mapping[str, JSON]:
        config: dict[str, JSON] = dict(kind=type(self).kind.get_config())
        if self.minimum is not None:
            config["minimum"] = self.minimum
        if self.maximum is not None:
            config["maximum"] = self.maximum
        return config

    @override
    def humanise(self, *, format: Format | LiteralFormat = Format.plain) -> str:
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
