"""
Maximum pointwise error-bounding requirements.
"""

import math
from collections.abc import Mapping
from dataclasses import dataclass
from typing import ClassVar, Self

from typing_extensions import override  # MSPV 3.12

from ...config import Format, LiteralFormat, _humanise_kinded_type, _parse_number
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
    \begin{align*}
    &R_{\text{max-pointwise-absolute-error-bound}(\epsilon_{\text{abs}})}(x_i, \hat{x}_i) \\
    &\quad := \begin{cases}
        \hat{x}_i \equiv \text{NaN} \quad &\text{if } x_i \equiv \text{NaN} \\
        \hat{x}_i = x_i \quad &\text{if } x_i \in \{ -\infty, \infty \} \\
        |\hat{x}_i - x_i| \leq \epsilon_{\text{abs}} \quad &\text{otherwise}
    \end{cases}
    \end{align*}
    \]

    The absolute error bound $\epsilon_{\text{abs}}$ must be non-negative and finite.

    Requirements $R$ are defined for each data point $x_i$ and its decompressed
    reconstruction $\hat{x}_i$, i.e. $R(x_i, \hat{x}_i)$.
    See the [`AnyRequirement`][....combinators.AnyRequirement] for more
    information.

    Parameters
    ----------
    value : int | float
        The non-negative and finite maximum pointwise absolute error bound.
    """

    kind: ClassVar[RequirementKind] = RequirementKind.max_pointwise_absolute_error_bound
    value: int | float

    def __init__(self, *, value: int | float) -> None:
        if value < 0:
            raise ValueError("error bound must be non-negative")
        if not math.isfinite(value):
            raise ValueError("error bound most be finite")

        self.value = value

    @override
    @classmethod
    def from_config(  # type: ignore
        cls,
        *,
        value: int | float,
    ) -> Self:
        """
        Construct the maximum pointwise absolute error bound requirement from its configuration.

        Parameters
        ----------
        value : int | float
            The non-negative and finite maximum pointwise absolute error bound.

        Returns
        -------
        requirement : Self
            The instantiated maximum pointwise absolute error bound
            requirement.
        """

        return cls(value=_parse_number(value))

    @override
    def get_config(self) -> Mapping[str, JSON]:
        """
        Get the configuration of this maximum pointwise absolute error bound requirement.

        Returns
        -------
        config : Mapping[str, JSON]
            Configuration in JSON object format.
        """

        return dict(kind=type(self).kind.get_config(), value=self.value)

    @override
    def humanise(self, *, format: Format | LiteralFormat = Format.plain) -> str:
        """
        Humanise the representation of this maximum pointwise absolute error bound requirement.

        Parameters
        ----------
        format : Format | LiteralFormat
            The format of the humanised representation.

        Returns
        -------
        humanised : str
            The humanised representation of this maximum pointwise absolute
            error bound requirement.
        """

        return f"{_humanise_kinded_type(self, format=format)}({self.value})"


@dataclass(kw_only=True, slots=True)
class MaxPointwiseRelativeErrorBoundRequirement(Requirement):
    r"""
    Require that the maximum pointwise relative error is bounded.

    \[
    \begin{align*}
    &R_{\text{max-pointwise-relative-error-bound}(\epsilon_{\text{rel}})}(x_i, \hat{x}_i) \\
    &\quad := \begin{cases}
        \hat{x}_i \equiv \text{NaN} \quad &\text{if } x_i \equiv \text{NaN} \\
        \hat{x}_i = x_i \quad &\text{if } x_i \in \{ -\infty, \infty \} \\
        |\hat{x}_i - x_i| \leq |x_i| \cdot \epsilon_{\text{rel}} \quad &\text{otherwise}
    \end{cases}
    \end{align*}
    \]

    The relative error bound $\epsilon_{\text{rel}}$ must be non-negative and finite.

    Requirements $R$ are defined for each data point $x_i$ and its decompressed
    reconstruction $\hat{x}_i$, i.e. $R(x_i, \hat{x}_i)$.
    See the [`AnyRequirement`][....combinators.AnyRequirement] for more
    information.

    Parameters
    ----------
    value : int | float
        The non-negative and finite maximum relative absolute error bound.
    """

    kind: ClassVar[RequirementKind] = RequirementKind.max_pointwise_relative_error_bound
    value: int | float

    def __init__(self, *, value: int | float) -> None:
        if value < 0:
            raise ValueError("error bound must be non-negative")
        if not math.isfinite(value):
            raise ValueError("error bound most be finite")

        self.value = value

    @override
    @classmethod
    def from_config(  # type: ignore
        cls,
        *,
        value: int | float,
    ) -> Self:
        """
        Construct the maximum pointwise relative error bound requirement from its configuration.

        Parameters
        ----------
        value : int | float
            The non-negative and finite maximum pointwise relative error bound.

        Returns
        -------
        requirement : Self
            The instantiated maximum pointwise relative error bound
            requirement.
        """

        return cls(value=_parse_number(value))

    @override
    def get_config(self) -> Mapping[str, JSON]:
        """
        Get the configuration of this maximum pointwise relative error bound requirement.

        Returns
        -------
        config : Mapping[str, JSON]
            Configuration in JSON object format.
        """

        return dict(kind=type(self).kind.get_config(), value=self.value)

    @override
    def humanise(self, *, format: Format | LiteralFormat = Format.plain) -> str:
        """
        Humanise the representation of this maximum pointwise relative error bound requirement.

        Parameters
        ----------
        format : Format | LiteralFormat
            The format of the humanised representation.

        Returns
        -------
        humanised : str
            The humanised representation of this maximum pointwise relative
            error bound requirement.
        """

        return f"{_humanise_kinded_type(self, format=format)}({self.value})"


@dataclass(kw_only=True, slots=True)
class MaxPointwiseRangeRelativeErrorBoundRequirement(Requirement):
    r"""
    Require that the maximum pointwise range-relative error is bounded.

    \[
    \begin{align*}
    &R_{\text{max-pointwise-range-relative-error-bound}(\epsilon_{\text{range-rel}})}(x_i, \hat{x}_i) \\
    &\quad := \begin{cases}
        \hat{x}_i \equiv \text{NaN} \quad &\text{if } x_i \equiv \text{NaN} \\
        \hat{x}_i = x_i \quad &\text{if } x_i \in \{ -\infty, \infty \} \\
        |\hat{x}_i - x_i| \leq x_{\text{range}} \cdot \epsilon_{\text{range-rel}} \quad &\text{otherwise}
    \end{cases}
    \end{align*}
    \]

    where

    \[
    \begin{align*}
        x_{\text{range}} &:= x_{\text{finite-max}} - x_{\text{finite-min}} \\
        x_{\text{finite-max}} &:= \max_i \{ x_i \mathbin{|} (x_i \not \equiv \text{NaN} \land x_i \not \in \{ -\infty, \infty \}) \} \\
        x_{\text{finite-min}} &:= \min_i \{ x_i \mathbin{|} (x_i \not \equiv \text{NaN} \land x_i \not \in \{ -\infty, \infty \}) \}
    \end{align*}
    \]

    The range-relative error bound $\epsilon_{\text{range-rel}}$ must be
    non-negative and finite.

    Requirements $R$ are defined for each data point $x_i$ and its decompressed
    reconstruction $\hat{x}_i$, i.e. $R(x_i, \hat{x}_i)$.
    See the [`AnyRequirement`][....combinators.AnyRequirement] for more
    information.

    Parameters
    ----------
    value : int | float
        The non-negative and finite maximum pointwise range-relative error
        bound.
    """

    kind: ClassVar[RequirementKind] = (
        RequirementKind.max_pointwise_range_relative_error_bound
    )
    value: int | float

    def __init__(self, *, value: int | float) -> None:
        if value < 0:
            raise ValueError("error bound must be non-negative")
        if not math.isfinite(value):
            raise ValueError("error bound most be finite")

        self.value = value

    @override
    @classmethod
    def from_config(  # type: ignore
        cls,
        *,
        value: int | float,
    ) -> Self:
        """
        Construct the maximum pointwise range-relative error bound requirement from its configuration.

        Parameters
        ----------
        value : int | float
            The non-negative and finite maximum pointwise range-relative error
            bound.

        Returns
        -------
        requirement : Self
            The instantiated maximum pointwise range-relative error bound
            requirement.
        """

        return cls(value=_parse_number(value))

    @override
    def get_config(self) -> Mapping[str, JSON]:
        """
        Get the configuration of this maximum pointwise range-relative error bound requirement.

        Returns
        -------
        config : Mapping[str, JSON]
            Configuration in JSON object format.
        """

        return dict(kind=type(self).kind.get_config(), value=self.value)

    @override
    def humanise(self, *, format: Format | LiteralFormat = Format.plain) -> str:
        """
        Humanise the representation of this maximum pointwise range-relative error bound requirement.

        Parameters
        ----------
        format : Format | LiteralFormat
            The format of the humanised representation.

        Returns
        -------
        humanised : str
            The humanised representation of this maximum pointwise
            range-relative error bound requirement.
        """

        return f"{_humanise_kinded_type(self, format=format)}({self.value})"


@dataclass(kw_only=True, slots=True)
class MaxPointwiseQuadraticErrorBoundRequirement(Requirement):
    r"""
    Require that the maximum pointwise quadratic error is bounded.

    \[
    \begin{align*}
    &R_{\text{max-pointwise-quadratic-error-bound}(\epsilon_{\text{qua}}, min, max)}(x_i, \hat{x}_i) \\
    &\quad := \begin{cases}
        \hat{x}_i \equiv \text{NaN} \quad &\text{if } x_i \equiv \text{NaN} \\
        \hat{x}_i = x_i \quad &\text{if } x_i \in \{ -\infty, \infty \} \\
        \hat{x}_i = x_i \quad &\text{if } x_i \leq min \lor x_i \geq max \\
        |\hat{x}_i - x_i| \leq \left(1 - {\left(2 \cdot \frac{x_i - min}{max - min} - 1\right)}^2 \right) \cdot \epsilon_{\text{qua}} \quad &\text{otherwise}
    \end{cases}
    \end{align*}
    \]

    The quadratic error bound $\epsilon_{\text{qua}}$ must be non-negative and
    finite.
    The limits `minimum` and `maximum` and their difference should be finite,
    with $max > min$, otherwise $\forall i \mathbin{.} (\hat{x}_i \equiv x_i)$.

    Requirements $R$ are defined for each data point $x_i$ and its decompressed
    reconstruction $\hat{x}_i$, i.e. $R(x_i, \hat{x}_i)$.
    See the [`AnyRequirement`][....combinators.AnyRequirement] for more
    information.

    Parameters
    ----------
    value : int | float
        The non-negative and finite maximum pointwise quadratic error bound.
    minimum : int | float
        The minimum for the quadratic error bound, at and below which data
        values are preserved exactly.
    maximum : int | float
        The maximum for the quadratic error bound, at and above which data
        values are preserved exactly.
    """

    kind: ClassVar[RequirementKind] = (
        RequirementKind.max_pointwise_quadratic_error_bound
    )
    value: int | float
    minimum: int | float
    maximum: int | float

    def __init__(
        self, *, value: int | float, minimum: int | float, maximum: int | float
    ) -> None:
        if value < 0:
            raise ValueError("error bound must be non-negative")
        if not math.isfinite(value):
            raise ValueError("error bound most be finite")
        if not math.isfinite(minimum):
            raise ValueError("minimum must be finite")
        if not math.isfinite(maximum):
            raise ValueError("maximum must be finite")
        if maximum <= minimum:
            raise ValueError("maximum must be greater than minimum")

        self.value = value
        self.minimum = minimum
        self.maximum = maximum

    @override
    @classmethod
    def from_config(  # type: ignore
        cls,
        *,
        value: int | float,
        minimum: int | float,
        maximum: int | float,
    ) -> Self:
        """
        Construct the maximum pointwise quadratic error bound requirement from its configuration.

        Parameters
        ----------
        value : int | float
            The non-negative and finite maximum pointwise quadratic error bound.
        minimum : int | float
            The minimum for the quadratic error bound, at and below which data
            values are preserved exactly.
        maximum : int | float
            The maximum for the quadratic error bound, at and above which data
            values are preserved exactly.

        Returns
        -------
        requirement : Self
            The instantiated maximum pointwise quadratic error bound
            requirement.
        """

        return cls(
            value=_parse_number(value),
            minimum=_parse_number(minimum),
            maximum=_parse_number(maximum),
        )

    @override
    def get_config(self) -> Mapping[str, JSON]:
        """
        Get the configuration of this maximum pointwise quadratic error bound requirement.

        Returns
        -------
        config : Mapping[str, JSON]
            Configuration in JSON object format.
        """

        return dict(
            kind=type(self).kind.get_config(),
            value=self.value,
            minimum=self.minimum,
            maximum=self.maximum,
        )

    @override
    def humanise(self, *, format: Format | LiteralFormat = Format.plain) -> str:
        """
        Humanise the representation of this maximum pointwise quadratic error bound requirement.

        Parameters
        ----------
        format : Format | LiteralFormat
            The format of the humanised representation.

        Returns
        -------
        humanised : str
            The humanised representation of this maximum pointwise quadratic
            error bound requirement.
        """

        return f"{_humanise_kinded_type(self, format=format)}({self.value}, minimum={self.minimum}, maximum={self.maximum})"
