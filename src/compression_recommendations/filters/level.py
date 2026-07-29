from collections.abc import Mapping
from dataclasses import dataclass
from enum import StrEnum
from typing import ClassVar, Literal, Self

from typing_extensions import override  # MSPV 3.12

from ..typing import JSON
from .abc import Filter
from .kind import FilterKind

__all__ = ["LevelKind", "LevelKindFilter"]


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


@dataclass(kw_only=True)
class LevelKindFilter(Filter):
    kind: ClassVar[FilterKind] = FilterKind.level_kind
    value: LevelKind

    def matches(
        self, *, markers: Mapping[str, None | bool | int | float | str]
    ) -> bool:
        if type(self).kind.value not in markers:
            return False
        return markers[type(self).kind.value] == self.value.value

    @override
    @classmethod
    def from_config(  # type: ignore
        cls,
        *,
        value: Literal["single"] | Literal["pressure"],
        kind: Literal["grib-short-name"] = FilterKind.grib_short_name.value,
    ) -> Self:
        return cls(value=LevelKind.from_config(value))

    @override
    def get_config(self) -> JSON:
        return dict(kind=type(self).kind.get_config(), value=self.value.get_config)
