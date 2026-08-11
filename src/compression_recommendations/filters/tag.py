"""
Filters for arbitrary tags.
"""

from collections.abc import Mapping
from dataclasses import dataclass
from typing import ClassVar, Literal, Self

from typing_extensions import override  # MSPV 3.12

from ..typing import JSON
from .abc import Filter
from .kind import FilterKind

__all__ = ["TagFilter"]


@dataclass(kw_only=True, slots=True)
class TagFilter(Filter):
    kind: ClassVar[FilterKind] = FilterKind.tag
    value: str

    def matches(
        self, *, markers: Mapping[str, None | bool | int | float | str]
    ) -> bool:
        if "tags" not in markers:
            return False
        tags = markers["tags"]
        if not isinstance(tags, str):
            return False
        return self.value in tags.split(",")

    @override
    @classmethod
    def from_config(  # type: ignore
        cls,
        *,
        value: str,
        kind: Literal["tag"] = FilterKind.tag.value,
    ) -> Self:
        return cls(value=value)

    @override
    def get_config(self) -> Mapping[str, JSON]:
        return dict(kind=type(self).kind.get_config(), value=self.value)

    @override
    def humanise(self) -> str:
        return f"{self.value!r} in tags"
