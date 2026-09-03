"""
Enumeration over all filter kinds.
"""

from enum import StrEnum
from typing import TYPE_CHECKING, Self, assert_never

if TYPE_CHECKING:
    from .abc import Filter

from ..typing import JSON

__all__ = ["FilterKind"]


class FilterKind(StrEnum):
    """
    Enumeration over all filter kinds.
    """

    any = "any"
    """ See the [`AnyFilter`][....combinators.AnyFilter]. """

    all = "all"
    """ See the [`AllFilters`][....combinators.AllFilters]. """

    cf_standard_name = "cf-standard-name"
    """ See the [`CfStandardNameFilter`][....cf.CfStandardNameFilter]. """

    cf_short_name = "cf-short-name"
    """ See the [`CfShortNameFilter`][....cf.CfShortNameFilter]. """

    grib_short_name = "grib-short-name"
    """ See the [`GribShortNameFilter`][....grib.GribShortNameFilter]. """

    level_kind = "level-kind"
    """ See the [`LevelKindFilter`][....level.LevelKindFilter]. """

    level_value = "level-value"
    """ See the [`LevelValueFilter`][....level.LevelValueFilter]. """

    tag = "tag"
    """ See the [`TagFilter`][....tag.TagFilter]. """

    @property
    def cls(self) -> type["Filter"]:
        """
        The concrete filter class associated with this filter kind.
        """

        match self:
            case FilterKind.any:
                from .combinators import AnyFilter  # noqa: PLC0415

                return AnyFilter
            case FilterKind.all:
                from .combinators import AllFilters  # noqa: PLC0415

                return AllFilters
            case FilterKind.cf_standard_name:
                from .cf import CfStandardNameFilter  # noqa: PLC0415

                return CfStandardNameFilter
            case FilterKind.cf_short_name:
                from .cf import CfShortNameFilter  # noqa: PLC0415

                return CfShortNameFilter
            case FilterKind.grib_short_name:
                from .grib import GribShortNameFilter  # noqa: PLC0415

                return GribShortNameFilter
            case FilterKind.level_kind:
                from .level import LevelKindFilter  # noqa: PLC0415

                return LevelKindFilter
            case FilterKind.level_value:
                from .level import LevelValueFilter  # noqa: PLC0415

                return LevelValueFilter
            case FilterKind.tag:
                from .tag import TagFilter  # noqa: PLC0415

                return TagFilter
            case _:
                assert_never(self)

    @classmethod
    def from_config(cls, *, kind: str) -> Self:
        """
        Construct the filter kind from its configuration.

        Parameters
        ----------
        kind : str
            The filter kind name.

        Returns
        -------
        kind : Self
            The instantiated filter kind.
        """

        return cls[kind.replace("-", "_")]

    def get_config(self) -> JSON:
        """
        Get the configuration of this filter kind.

        Returns
        -------
        config : JSIN
            Configuration in JSON format.
        """

        return self.value
