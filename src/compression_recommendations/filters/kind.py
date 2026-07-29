from enum import StrEnum
from typing import Self

from ..typing import JSON

__all__ = ["FilterKind"]


class FilterKind(StrEnum):
    any = "any"
    all = "all"
    cf_standard_name = "cf-standard-name"
    cf_short_name = "cf-short-name"
    grib_short_name = "grib-short-name"
    level_kind = "level-kind"

    @classmethod
    def from_config(cls, kind: str) -> Self:
        return cls[kind.replace("-", "_")]

    def get_config(self) -> JSON:
        return self.value
