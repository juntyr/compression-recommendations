"""
Lossless compression requirement.
"""

from collections.abc import Mapping
from dataclasses import dataclass
from typing import ClassVar, Literal, Self

from typing_extensions import override  # MSPV 3.12

from ..config import Format, LiteralFormat, _humanise_kinded_type
from ..typing import JSON
from .abc import Requirement
from .kind import RequirementKind

__all__ = ["LosslessRequirement"]


@dataclass(kw_only=True, slots=True)
class LosslessRequirement(Requirement):
    r"""
    Require that data is preserved exactly.

    \[
    R_{\text{lossless}}(x_i, \hat{x}_i) := bits(x_i) = bits(\hat{x}_i)
    \]

    Requirements $R$ are defined for each data point $x_i$ and its decompressed
    reconstruction $\hat{x}_i$, i.e. $R(x_i, \hat{x}_i)$.
    See the [`AnyRequirement`][...combinators.AnyRequirement] for more
    information.
    """

    kind: ClassVar[RequirementKind] = RequirementKind.lossless

    @override
    @classmethod
    def from_config(  # type: ignore
        cls,
        *,
        kind: Literal["lossless"] = RequirementKind.lossless.value,
    ) -> Self:
        return cls()

    @override
    def get_config(self) -> Mapping[str, JSON]:
        return dict(kind=type(self).kind.get_config())

    @override
    def humanise(self, *, format: Format | LiteralFormat = Format.plain) -> str:
        return f"{_humanise_kinded_type(self, format=format)}"
