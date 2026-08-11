"""
Filters for vertical levels.
"""

from collections.abc import Mapping
from dataclasses import dataclass
from enum import StrEnum
from typing import ClassVar, Literal, Self

from typing_extensions import override  # MSPV 3.12

from ..config import _parse_number
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


@dataclass(kw_only=True, slots=True)
class LevelKindFilter(Filter):
    kind: ClassVar[FilterKind] = FilterKind.level_kind
    value: LevelKind

    def matches(
        self, *, markers: Mapping[str, None | bool | int | float | str]
    ) -> bool:
        if type(self).kind.value not in markers:
            return False
        return markers[type(self).kind.value] == self.value.value

    @classmethod
    def marker_for(
        cls, value: LevelKind
    ) -> Mapping[str, None | bool | int | float | str]:
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


@dataclass(kw_only=True, slots=True)
class LevelValueFilter(Filter):
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
    def marker_for(
        cls, value: int | float
    ) -> Mapping[str, None | bool | int | float | str]:
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
