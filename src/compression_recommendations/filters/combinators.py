"""
Logical combinations of multiple filters.
"""

from collections.abc import Collection, Mapping
from dataclasses import dataclass
from typing import ClassVar, Literal, Self

from typing_extensions import override  # MSPV 3.12

from ..typing import JSON
from .abc import Filter
from .kind import FilterKind

__all__ = ["AnyFilter", "AllFilters"]


@dataclass(kw_only=True)
class AnyFilter(Filter):
    kind: ClassVar[FilterKind] = FilterKind.any
    filters: Collection[Filter]

    def matches(
        self, *, markers: Mapping[str, None | bool | int | float | str]
    ) -> bool:
        any_match = False

        for filter in self.filters:
            any_match |= filter.matches(markers=markers)

        return any_match

    @override
    @classmethod
    def from_config(  # type: ignore
        cls,
        *,
        filters: Collection[Mapping[str, JSON]],
        kind: Literal["any"] = FilterKind.any.value,
    ) -> Self:
        return cls(
            filters=tuple(
                Filter.from_config(
                    **filter  # type: ignore
                )
                for filter in filters
            )
        )

    @override
    def get_config(self) -> JSON:
        return dict(
            kind=type(self).kind.get_config(),
            filters=tuple(filter.get_config() for filter in self.filters),
        )


@dataclass(kw_only=True)
class AllFilters(Filter):
    kind: ClassVar[FilterKind] = FilterKind.all
    filters: Collection[Filter]

    def matches(
        self, *, markers: Mapping[str, None | bool | int | float | str]
    ) -> bool:
        all_match = True

        for filter in self.filters:
            all_match &= filter.matches(markers=markers)

        return all_match

    @override
    @classmethod
    def from_config(  # type: ignore
        cls,
        *,
        filters: Collection[Mapping[str, JSON]],
        kind: Literal["all"] = FilterKind.all.value,
    ) -> Self:
        return cls(
            filters=tuple(
                Filter.from_config(
                    **filter  # type: ignore
                )
                for filter in filters
            )
        )

    @override
    def get_config(self) -> JSON:
        return dict(
            kind=type(self).kind.get_config(),
            filters=tuple(filter.get_config() for filter in self.filters),
        )
