"""
Filters for GRIB metadata attributes.
"""

from collections.abc import Mapping
from dataclasses import dataclass
from typing import ClassVar, Literal, Self

from typing_extensions import override  # MSPV 3.12

from ..config import Format, LiteralFormat, _humanise_kinded_type
from ..typing import JSON
from .abc import Filter
from .kind import FilterKind

__all__ = ["GribShortNameFilter"]


@dataclass(kw_only=True, slots=True)
class GribShortNameFilter(Filter):
    kind: ClassVar[FilterKind] = FilterKind.grib_short_name
    value: str

    def matches(
        self, *, markers: Mapping[str, None | bool | int | float | str]
    ) -> bool:
        if type(self).kind.value not in markers:
            return False
        return markers[type(self).kind.value] == self.value

    @classmethod
    def marker_for(cls, value: str) -> Mapping[str, None | bool | int | float | str]:
        return {cls.kind.value: value}

    @override
    @classmethod
    def from_config(  # type: ignore
        cls,
        *,
        value: str,
        kind: Literal["grib-short-name"] = FilterKind.grib_short_name.value,
    ) -> Self:
        return cls(value=value)

    @override
    def get_config(self) -> Mapping[str, JSON]:
        return dict(kind=type(self).kind.get_config(), value=self.value)

    @override
    def humanise(self, *, format: Format | LiteralFormat = Format.plain) -> str:
        return f"{_humanise_kinded_type(self, format=format)}({self.value})"
