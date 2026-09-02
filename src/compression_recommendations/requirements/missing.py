"""
Missing value preserving requirements.
"""

from collections.abc import Mapping
from dataclasses import dataclass
from typing import ClassVar, Literal, Self

from typing_extensions import override  # MSPV 3.12

from ..config import Format, LiteralFormat, _humanise_kinded_type, _parse_number
from ..typing import JSON
from .abc import Requirement
from .kind import RequirementKind

__all__ = ["MissingValueRequirement"]


@dataclass(kw_only=True, slots=True)
class MissingValueRequirement(Requirement):
    r"""
    Require that the missing `value` sentinel is preserved.

    \[
    R_{\text{missing-value}(v)}(x_i, \hat{x}_i) := (\hat{x}_i \equiv v) \iff (x_i \equiv v)
    \]

    The equivalence relationship $x_i \equiv v$ holds when $x_i = v$ and also for
    $-0.0 \equiv +0.0$ and $\text{NaN} \equiv \text{NaN}$.

    Requirements $R$ are defined for each data point $x_i$ and its decompressed
    reconstruction $\hat{x}_i$, i.e. $R(x_i, \hat{x}_i)$.
    See the [`AnyRequirement`][...combinators.AnyRequirement] for more
    information.

    Parameters
    ----------
    value : int | float
        The missing value sentinel to preserve.
    """

    kind: ClassVar[RequirementKind] = RequirementKind.missing_value
    value: int | float

    @override
    @classmethod
    def from_config(  # type: ignore
        cls,
        *,
        value: int | float,
        kind: Literal["missing-value"] = RequirementKind.missing_value.value,
    ) -> Self:
        return cls(value=_parse_number(value))

    @override
    def get_config(self) -> Mapping[str, JSON]:
        return dict(kind=type(self).kind.get_config(), value=self.value)

    @override
    def humanise(self, *, format: Format | LiteralFormat = Format.plain) -> str:
        return f"{_humanise_kinded_type(self, format=format)}({self.value})"
