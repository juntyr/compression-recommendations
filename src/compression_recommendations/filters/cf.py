"""
Filters for CF metadata attributes.
"""

from collections.abc import Mapping
from dataclasses import dataclass
from typing import ClassVar, Literal, Self

from typing_extensions import override  # MSPV 3.12

from ..typing import JSON
from .abc import Filter
from .kind import FilterKind

__all__ = ["CfStandardNameFilter", "CfShortNameFilter"]


@dataclass(kw_only=True, slots=True)
class CfStandardNameFilter(Filter):
    kind: ClassVar[FilterKind] = FilterKind.cf_standard_name
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
        kind: Literal["cf-standard-name"] = FilterKind.cf_standard_name.value,
    ) -> Self:
        return cls(value=value)

    @override
    def get_config(self) -> Mapping[str, JSON]:
        return dict(kind=type(self).kind.get_config(), value=self.value)


@dataclass(kw_only=True, slots=True)
class CfShortNameFilter(Filter):
    kind: ClassVar[FilterKind] = FilterKind.cf_short_name
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
        kind: Literal["cf-short-name"] = FilterKind.cf_short_name.value,
    ) -> Self:
        return cls(value=value)

    @override
    def get_config(self) -> Mapping[str, JSON]:
        return dict(kind=type(self).kind.get_config(), value=self.value)
