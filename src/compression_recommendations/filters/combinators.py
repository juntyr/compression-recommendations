"""
Logical combinations of multiple filters.
"""

from collections.abc import Collection, Mapping
from dataclasses import dataclass
from typing import ClassVar, Literal, Self

from typing_extensions import override  # MSPV 3.12

from ..config import Format, LiteralFormat, _humanise_labelled_type
from ..typing import JSON
from .abc import Filter
from .kind import FilterKind

__all__ = ["AnyFilter", "AllFilters"]


@dataclass(kw_only=True, slots=True)
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
    def get_config(self) -> Mapping[str, JSON]:
        return dict(
            kind=type(self).kind.get_config(),
            filters=[filter.get_config() for filter in self.filters],
        )

    @override
    def humanise(self, *, format: Format | LiteralFormat = Format.plain) -> str:
        match self.filters:
            case ():
                return _humanise_labelled_type(self, label="False", format=format)
            case (filter,):
                return filter.humanise(format=format)
            case filters:
                or_ = _humanise_labelled_type(self, label="or", format=format)
                return f"({f' {or_} '.join(filter.humanise(format=format) for filter in filters)})"


@dataclass(kw_only=True, slots=True)
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
    def get_config(self) -> Mapping[str, JSON]:
        return dict(
            kind=type(self).kind.get_config(),
            filters=[filter.get_config() for filter in self.filters],
        )

    @override
    def humanise(self, *, format: Format | LiteralFormat = Format.plain) -> str:
        match self.filters:
            case ():
                return _humanise_labelled_type(self, label="True", format=format)
            case (filter,):
                return filter.humanise(format=format)
            case filters:
                and_ = _humanise_labelled_type(self, label="and", format=format)
                return f"({f' {and_} '.join(filter.humanise(format=format) for filter in filters)})"
