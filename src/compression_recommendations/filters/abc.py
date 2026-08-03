"""
Abstract base class for filters.
"""

from abc import ABC, abstractmethod
from collections.abc import Mapping
from typing import ClassVar, Self, assert_never

from typing_extensions import override  # MSPV 3.12

from ..config import Config
from ..typing import JSON
from .kind import FilterKind

__all__ = ["Filter"]


class Filter(Config, ABC):
    __slots__: tuple[str, ...] = ("kind",)

    kind: ClassVar[FilterKind]

    @abstractmethod
    def matches(
        self, *, markers: Mapping[str, None | bool | int | float | str]
    ) -> bool:
        pass

    @override
    @classmethod
    def from_config(cls, *, kind: str, **kwargs: JSON) -> Self:  # type: ignore
        from .cf import CfShortNameFilter, CfStandardNameFilter  # noqa: PLC0415
        from .combinators import AllFilters, AnyFilter  # noqa: PLC0415
        from .grib import GribShortNameFilter  # noqa: PLC0415
        from .level import LevelKindFilter, LevelValueFilter  # noqa: PLC0415
        from .tag import TagFilter  # noqa: PLC0415

        kind_ = FilterKind.from_config(kind)
        match kind_:
            case FilterKind.any:
                return AnyFilter.from_config(
                    **kwargs  # type: ignore
                )
            case FilterKind.all:
                return AllFilters.from_config(
                    **kwargs  # type: ignore
                )
            case FilterKind.cf_standard_name:
                return CfStandardNameFilter.from_config(
                    **kwargs  # type: ignore
                )
            case FilterKind.cf_short_name:
                return CfShortNameFilter.from_config(
                    **kwargs  # type: ignore
                )
            case FilterKind.grib_short_name:
                return GribShortNameFilter.from_config(
                    **kwargs  # type: ignore
                )
            case FilterKind.level_kind:
                return LevelKindFilter.from_config(
                    **kwargs  # type: ignore
                )
            case FilterKind.level_value:
                return LevelValueFilter.from_config(
                    **kwargs  # type: ignore
                )
            case FilterKind.tag:
                return TagFilter.from_config(
                    **kwargs  # type: ignore
                )
            case _:
                assert_never(kind_)
