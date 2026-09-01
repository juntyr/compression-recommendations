"""
Data limit-preserving requirements.
"""

from collections.abc import Mapping
from dataclasses import dataclass
from typing import ClassVar, Literal, Self, assert_never

from typing_extensions import override  # MSPV 3.12

from ..config import Format, LiteralFormat, _humanise_kinded_type, _parse_number
from ..typing import JSON
from .abc import Requirement
from .kind import RequirementKind

__all__ = ["DataLimitsRequirement"]


@dataclass(kw_only=True, slots=True)
class DataLimitsRequirement(Requirement):
    r"""
    Require that the decompressed data stays within the given `minimum` and `maximum` limits.

    \[
    \begin{align}
        R_{\text{data-limits}(min=\texttt{None}, max=\texttt{None})}(x_i, \hat{x}_i) &:= \top \tag{1} \\
        R_{\text{data-limits}(min, max=\texttt{None})}(x_i, \hat{x}_i) &:= min \leq \hat{x}_i \quad \text{if } x_i \geq min \tag{2a} \\
        R_{\text{data-limits}(min, max=\texttt{None})}(x_i, \hat{x}_i) &:= \top \quad \text{otherwise} \tag{2b} \\
        R_{\text{data-limits}(min=\texttt{None}, max)}(x_i, \hat{x}_i) &:= \hat{x}_i \leq max \quad \text{if } x_i \leq max \tag{3a} \\
        R_{\text{data-limits}(min=\texttt{None}, max)}(x_i, \hat{x}_i) &:= \top \quad \text{otherwise} \tag{3b} \\
        R_{\text{data-limits}(min, max)}(x_i, \hat{x}_i) &:= min \leq \hat{x}_i \leq max \quad \text{if } min \leq x_i \leq max \tag{4a} \\
        R_{\text{data-limits}(min, max)}(x_i, \hat{x}_i) &:= \top \quad \text{otherwise} \tag{4b}
    \end{align}
    \]

    If an original data value $x_i$ is not within the limits, no requirement is
    imposed on the decompressed data value $\hat{x}_i$.

    Requirements $R$ are defined for each data point $x_i$ and its decompressed
    reconstruction $\hat{x}_i$, i.e. $R(x_i, \hat{x}_i)$.
    See the [`AnyRequirement`][...combinators.AnyRequirement] for more
    information.
    """

    kind: ClassVar[RequirementKind] = RequirementKind.data_limits
    minimum: None | int | float = None
    maximum: None | int | float = None

    @override
    @classmethod
    def from_config(  # type: ignore
        cls,
        *,
        minimum: None | int | float = None,
        maximum: None | int | float = None,
        kind: Literal["data-limits"] = RequirementKind.data_limits.value,
    ) -> Self:
        return cls(
            minimum=None if minimum is None else _parse_number(minimum),
            maximum=None if maximum is None else _parse_number(maximum),
        )

    @override
    def get_config(self) -> Mapping[str, JSON]:
        config: dict[str, JSON] = dict(kind=type(self).kind.get_config())
        if self.minimum is not None:
            config["minimum"] = self.minimum
        if self.maximum is not None:
            config["maximum"] = self.maximum
        return config

    @override
    def humanise(self, *, format: Format | LiteralFormat = Format.plain) -> str:
        ty = _humanise_kinded_type(self, format=format)
        limits = (self.minimum, self.maximum)
        match limits:
            case (None, None):
                return f"{ty}()"
            case (minimum, None):
                return f"{ty}(minimum={minimum})"
            case (None, maximum):
                return f"{ty}(maximum={maximum})"
            case (minimum, maximum):
                return f"{ty}(minimum={minimum}, maximum={maximum})"
            case _:
                assert_never(limits)
