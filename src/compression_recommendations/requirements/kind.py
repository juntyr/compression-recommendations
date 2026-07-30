from enum import StrEnum
from typing import Self

from ..typing import JSON

__all__ = ["RequirementKind"]


class RequirementKind(StrEnum):
    any = "any"
    all = "all"
    max_pointwise_absolute_error_bound = "max-pointwise-absolute-error-bound"
    mean_absolute_error_bound = "mean-absolute-error-bound"
    max_pointwise_relative_error_bound = "max-pointwise-relative-error-bound"
    mean_relative_error_bound = "mean-relative-error-bound"
    global_minimum = "global-minimum"
    global_maximum = "global-maximum"

    @classmethod
    def from_config(cls, kind: str) -> Self:
        return cls[kind.replace("-", "_")]

    def get_config(self) -> JSON:
        return self.value
