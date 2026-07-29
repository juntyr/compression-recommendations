from collections.abc import Mapping
from dataclasses import dataclass
from typing import ClassVar, Literal, Self, override

from ..typing import JSON
from .abc import Filter
from .kind import FilterKind

__all__ = ["GribShortNameFilter"]


@dataclass(kw_only=True)
class GribShortNameFilter(Filter):
    kind: ClassVar[FilterKind] = FilterKind.grib_short_name
    value: str

    def matches(
        self, *, markers: Mapping[str, None | bool | int | float | str]
    ) -> bool:
        if type(self).kind.value not in markers:
            return False
        return markers[type(self).kind.value] == self.value

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
    def get_config(self) -> JSON:
        return dict(kind=type(self).kind.get_config(), value=self.value)
