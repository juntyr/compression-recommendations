"""
Maximum pointwise error-bounding requirements.
"""

from collections.abc import Mapping
from dataclasses import dataclass
from typing import ClassVar, Literal, Self

from typing_extensions import override  # MSPV 3.12

from ...config import _parse_number, _to_camel_case
from ...typing import JSON
from ..abc import Requirement
from ..kind import RequirementKind

__all__ = [
    "MaxPointwiseAbsoluteErrorBoundRequirement",
    "MaxPointwiseRelativeErrorBoundRequirement",
    "MaxPointwiseRangeRelativeErrorBoundRequirement",
    "MaxPointwiseQuadraticErrorBoundRequirement",
]


@dataclass(kw_only=True, slots=True)
class MaxPointwiseAbsoluteErrorBoundRequirement(Requirement):
    r"""
    Require that the maximum pointwise absolute error is bounded.

    \[
    R_{\text{\tiny max-pointwise-absolute-error-bound}(\epsilon_{\text{abs}})}(x_i, \hat{x}_i) := \begin{cases}
        \hat{x}_i \equiv \text{NaN} \quad &\text{if } x_i \equiv \text{NaN} \\
        \hat{x}_i = x_i \quad &\text{if } x_i \in \{ -\infty, \infty \} \\
        |\hat{x}_i - x_i| \leq \epsilon_{\text{abs}} \quad &\text{otherwise}
    \end{cases}
    \]

    The absolute error bound $\epsilon_{\text{abs}}$ must be non-negative and finite.

    Requirements $R$ are defined for each data point $x_i$ and its decompressed
    reconstruction $\hat{x}_i$, i.e. $R(x_i, \hat{x}_i)$.
    See the [`AnyRequirement`][....combinators.AnyRequirement] for more
    information.
    """

    kind: ClassVar[RequirementKind] = RequirementKind.max_pointwise_absolute_error_bound
    value: int | float

    @override
    @classmethod
    def from_config(  # type: ignore
        cls,
        *,
        value: int | float,
        kind: Literal[
            "max-pointwise-absolute-error-bound"
        ] = RequirementKind.max_pointwise_absolute_error_bound.value,
    ) -> Self:
        return cls(value=_parse_number(value))

    @override
    def get_config(self) -> Mapping[str, JSON]:
        return dict(kind=type(self).kind.get_config(), value=self.value)

    @override
    def humanise(self) -> str:
        return f"{_to_camel_case(type(self).kind)}({self.value})"


@dataclass(kw_only=True, slots=True)
class MaxPointwiseRelativeErrorBoundRequirement(Requirement):
    r"""
    Require that the maximum pointwise relative error is bounded.

    \[
    R_{\text{\tiny max-pointwise-relative-error-bound}(\epsilon_{\text{rel}})}(x_i, \hat{x}_i) := \begin{cases}
        \hat{x}_i \equiv \text{NaN} \quad &\text{if } x_i \equiv \text{NaN} \\
        \hat{x}_i = x_i \quad &\text{if } x_i \in \{ -\infty, \infty \} \\
        |\hat{x}_i - x_i| \leq |x_i| \cdot \epsilon_{\text{rel}} \quad &\text{otherwise}
    \end{cases}
    \]

    The relative error bound $\epsilon_{\text{rel}}$ must be non-negative and finite.

    Requirements $R$ are defined for each data point $x_i$ and its decompressed
    reconstruction $\hat{x}_i$, i.e. $R(x_i, \hat{x}_i)$.
    See the [`AnyRequirement`][....combinators.AnyRequirement] for more
    information.
    """

    kind: ClassVar[RequirementKind] = RequirementKind.max_pointwise_relative_error_bound
    value: int | float

    @override
    @classmethod
    def from_config(  # type: ignore
        cls,
        *,
        value: int | float,
        kind: Literal[
            "max-pointwise-relative-error-bound"
        ] = RequirementKind.max_pointwise_relative_error_bound.value,
    ) -> Self:
        return cls(value=_parse_number(value))

    @override
    def get_config(self) -> Mapping[str, JSON]:
        return dict(kind=type(self).kind.get_config(), value=self.value)

    @override
    def humanise(self) -> str:
        return f"{_to_camel_case(type(self).kind)}({self.value})"


@dataclass(kw_only=True, slots=True)
class MaxPointwiseRangeRelativeErrorBoundRequirement(Requirement):
    r"""
    Require that the maximum pointwise range-relative error is bounded.

    \[
    R_{\text{\tiny max-pointwise-range-relative-error-bound}(\epsilon_{\text{range-rel}})}(x_i, \hat{x}_i) := \begin{cases}
        \hat{x}_i \equiv \text{NaN} \quad &\text{if } x_i \equiv \text{NaN} \\
        \hat{x}_i = x_i \quad &\text{if } x_i \in \{ -\infty, \infty \} \\
        |\hat{x}_i - x_i| \leq x_{\text{range}} \cdot \epsilon_{\text{range-rel}} \quad &\text{otherwise}
    \end{cases}
    \]

    where

    \[
    \begin{align*}
        x_{\text{range}} &:= x_{\text{finite-max}} - x_{\text{finite-min}} \\
        x_{\text{finite-max}} &:= \max_i \{ x_i \mathbin{|} x_i \not \equiv \text{NaN} \land x_i \not \in \{ -\infty, \infty \} \} \\
        x_{\text{finite-min}} &:= \min_i \{ x_i \mathbin{|} x_i \not \equiv \text{NaN} \land x_i \not \in \{ -\infty, \infty \} \}
    \end{align*}
    \]

    The range-relative error bound $\epsilon_{\text{range-rel}}$ must be
    non-negative and finite.

    Requirements $R$ are defined for each data point $x_i$ and its decompressed
    reconstruction $\hat{x}_i$, i.e. $R(x_i, \hat{x}_i)$.
    See the [`AnyRequirement`][....combinators.AnyRequirement] for more
    information.
    """

    kind: ClassVar[RequirementKind] = (
        RequirementKind.max_pointwise_range_relative_error_bound
    )
    value: int | float

    @override
    @classmethod
    def from_config(  # type: ignore
        cls,
        *,
        value: int | float,
        kind: Literal[
            "max-pointwise-range-relative-error-bound"
        ] = RequirementKind.max_pointwise_range_relative_error_bound.value,
    ) -> Self:
        return cls(value=_parse_number(value))

    @override
    def get_config(self) -> Mapping[str, JSON]:
        return dict(kind=type(self).kind.get_config(), value=self.value)

    @override
    def humanise(self) -> str:
        return f"{_to_camel_case(type(self).kind)}({self.value})"


@dataclass(kw_only=True, slots=True)
class MaxPointwiseQuadraticErrorBoundRequirement(Requirement):
    kind: ClassVar[RequirementKind] = (
        RequirementKind.max_pointwise_quadratic_error_bound
    )
    value: int | float
    minimum: int | float
    maximum: int | float

    @override
    @classmethod
    def from_config(  # type: ignore
        cls,
        *,
        value: int | float,
        minimum: int | float,
        maximum: int | float,
        kind: Literal[
            "max-pointwise-quadratic-error-bound"
        ] = RequirementKind.max_pointwise_quadratic_error_bound.value,
    ) -> Self:
        return cls(
            value=_parse_number(value),
            minimum=_parse_number(minimum),
            maximum=_parse_number(maximum),
        )

    @override
    def get_config(self) -> Mapping[str, JSON]:
        return dict(
            kind=type(self).kind.get_config(),
            value=self.value,
            minimum=self.minimum,
            maximum=self.maximum,
        )

    @override
    def humanise(self) -> str:
        return f"{_to_camel_case(type(self).kind)}({self.value}, minimum={self.minimum}, maximum={self.maximum})"
