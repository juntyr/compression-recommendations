"""
Mean error-bounding requirements.
"""

from collections.abc import Mapping
from dataclasses import dataclass
from typing import ClassVar, Self

from typing_extensions import override  # MSPV 3.12

from ...config import Format, LiteralFormat, _humanise_kinded_type, _parse_number
from ...typing import JSON
from ..abc import Requirement
from ..kind import RequirementKind

__all__ = [
    "MeanAbsoluteErrorBoundRequirement",
    "MeanRelativeErrorBoundRequirement",
    "MeanRangeRelativeErrorBoundRequirement",
]


@dataclass(kw_only=True, slots=True)
class MeanAbsoluteErrorBoundRequirement(Requirement):
    r"""
    Require that the mean absolute error is bounded.

    \[
    \begin{align*}
    &R_{\text{mean-absolute-error-bound}(\epsilon_{\text{mean-abs}})}(x_i, \hat{x}_i) \\
    &\quad := \begin{cases}
        \hat{x}_i \equiv \text{NaN} \quad &\text{if } x_i \equiv \text{NaN} \\
        \hat{x}_i = x_i \quad &\text{if } x_i \in \{ -\infty, \infty \} \\
        \Epsilon_{\text{mean-absolute}}(x, \hat{x}) \leq \epsilon_{\text{mean-abs}} \quad &\text{otherwise}
    \end{cases}
    \end{align*}
    \]

    where

    \[
    \Epsilon_{\text{mean-absolute}}(x, \hat{x}) := \frac{\sum_{i} \{ (|\hat{x}_i - x_i|) \mathbin{|} (x_i \not \equiv \text{NaN} \land x_i \not \in \{ -\infty, \infty \}) \}}{\sum_{i} \{ 1 \mathbin{|} (x_i \not \equiv \text{NaN} \land x_i \not \in \{ -\infty, \infty \}) \}}
    \]

    The absolute error bound $\epsilon_{\text{mean-abs}}$ must be non-negative
    and finite.

    Requirements $R$ are defined for each data point $x_i$ and its decompressed
    reconstruction $\hat{x}_i$, i.e. $R(x_i, \hat{x}_i)$.
    See the [`AnyRequirement`][....combinators.AnyRequirement] for more
    information.

    Parameters
    ----------
    value : int | float
        The non-negative and finite mean absolute error bound.
    """

    kind: ClassVar[RequirementKind] = RequirementKind.mean_absolute_error_bound
    value: int | float

    @override
    @classmethod
    def from_config(  # type: ignore
        cls,
        *,
        value: int | float,
    ) -> Self:
        """
        Construct the mean absolute error bound requirement from its configuration.

        Parameters
        ----------
        value : int | float
            The non-negative and finite mean absolute error bound.

        Returns
        -------
        requirement : Self
            The instantiated mean absolute error bound requirement.
        """

        return cls(value=_parse_number(value))

    @override
    def get_config(self) -> Mapping[str, JSON]:
        """
        Get the configuration of this mean absolute error bound requirement.

        Returns
        -------
        config : Mapping[str, JSON]
            Configuration in JSON object format.
        """

        return dict(kind=type(self).kind.get_config(), value=self.value)

    @override
    def humanise(self, *, format: Format | LiteralFormat = Format.plain) -> str:
        """
        Humanise the representation of this mean absolute error bound requirement.

        Parameters
        ----------
        format : Format | LiteralFormat
            The format of the humanised representation.

        Returns
        -------
        humanised : str
            The humanised representation of this mean absolute error bound
            requirement.
        """

        return f"{_humanise_kinded_type(self, format=format)}({self.value})"


@dataclass(kw_only=True, slots=True)
class MeanRelativeErrorBoundRequirement(Requirement):
    r"""
    Require that the mean relative error is bounded.

    \[
    \begin{align*}
    &R_{\text{mean-relative-error-bound}(\epsilon_{\text{mean-rel}})}(x_i, \hat{x}_i) \\
    &\quad := \begin{cases}
        \hat{x}_i \equiv \text{NaN} \quad &\text{if } x_i \equiv \text{NaN} \\
        \hat{x}_i = x_i \quad &\text{if } x_i \in \{ -\infty, \infty \} \\
        \hat{x}_i = x_i \quad &\text{if } x_i \in \{ -0.0, +0.0 \} \\
        \Epsilon_{\text{sum-absolute}}(x, \hat{x}) \leq B_{\text{sum-relative}}(x, \epsilon_{\text{mean-rel}}) \quad &\text{otherwise}
    \end{cases}
    \end{align*}
    \]

    where

    \[
    \begin{align*}
    \Epsilon_{\text{sum-absolute}}(x, \hat{x}) &:= \sum_{i} \{ (|\hat{x}_i - x_i|) \mathbin{|} (x_i \not \equiv \text{NaN} \land x_i \not \in \{ -\infty, \infty \}) \} \\
    B_{\text{sum-relative}}(x, \epsilon_{\text{mean-rel}}) &:= \sum_{i} \{ (|x_i| \cdot \epsilon_{\text{mean-rel}}) \mathbin{|} (x_i \not \equiv \text{NaN} \land x_i \not \in \{ -\infty, \infty \}) \}
    \end{align*}
    \]

    The relative error bound $\epsilon_{\text{mean-rel}}$ must be non-negative
    and finite.

    Requirements $R$ are defined for each data point $x_i$ and its decompressed
    reconstruction $\hat{x}_i$, i.e. $R(x_i, \hat{x}_i)$.
    See the [`AnyRequirement`][....combinators.AnyRequirement] for more
    information.

    Parameters
    ----------
    value : int | float
        The non-negative and finite mean relative error bound.
    """

    kind: ClassVar[RequirementKind] = RequirementKind.mean_relative_error_bound
    value: int | float

    @override
    @classmethod
    def from_config(  # type: ignore
        cls,
        *,
        value: int | float,
    ) -> Self:
        """
        Construct the mean relative error bound requirement from its configuration.

        Parameters
        ----------
        value : int | float
            The non-negative and finite mean relative error bound.

        Returns
        -------
        requirement : Self
            The instantiated mean relative error bound requirement.
        """

        return cls(value=_parse_number(value))

    @override
    def get_config(self) -> Mapping[str, JSON]:
        """
        Get the configuration of this mean relative error bound requirement.

        Returns
        -------
        config : Mapping[str, JSON]
            Configuration in JSON object format.
        """

        return dict(kind=type(self).kind.get_config(), value=self.value)

    @override
    def humanise(self, *, format: Format | LiteralFormat = Format.plain) -> str:
        """
        Humanise the representation of this mean relative error bound requirement.

        Parameters
        ----------
        format : Format | LiteralFormat
            The format of the humanised representation.

        Returns
        -------
        humanised : str
            The humanised representation of this mean relative error bound
            requirement.
        """

        return f"{_humanise_kinded_type(self, format=format)}({self.value})"


@dataclass(kw_only=True, slots=True)
class MeanRangeRelativeErrorBoundRequirement(Requirement):
    r"""
    Require that the mean range-relative error is bounded.

    \[
    \begin{align*}
    &R_{\text{mean-range-relative-error-bound}(\epsilon_{\text{mean-range-rel}})}(x_i, \hat{x}_i) \\
    &\quad := \begin{cases}
        \hat{x}_i \equiv \text{NaN} \quad &\text{if } x_i \equiv \text{NaN} \\
        \hat{x}_i = x_i \quad &\text{if } x_i \in \{ -\infty, \infty \} \\
        \Epsilon_{\text{mean-absolute}}(x, \hat{x}) \leq x_{\text{range}} \cdot \epsilon_{\text{mean-range-rel}} \quad &\text{otherwise}
    \end{cases}
    \end{align*}
    \]

    where

    \[
    \begin{align*}
    \Epsilon_{\text{mean-absolute}}(x, \hat{x}) &:= \frac{\sum_{i} \{ (|\hat{x}_i - x_i|) \mathbin{|} (x_i \not \equiv \text{NaN} \land x_i \not \in \{ -\infty, \infty \}) \}}{\sum_{i} \{ 1 \mathbin{|} (x_i \not \equiv \text{NaN} \land x_i \not \in \{ -\infty, \infty \}) \}} \\
    x_{\text{range}} &:= x_{\text{finite-max}} - x_{\text{finite-min}} \\
    x_{\text{finite-max}} &:= \max_i \{ x_i \mathbin{|} x_i \not \equiv \text{NaN} \land x_i \not \in \{ -\infty, \infty \} \} \\
    x_{\text{finite-min}} &:= \min_i \{ x_i \mathbin{|} x_i \not \equiv \text{NaN} \land x_i \not \in \{ -\infty, \infty \} \}
    \end{align*}
    \]

    The range-relative error bound $\epsilon_{\text{mean-range-rel}}$ must be
    non-negative and finite.

    Requirements $R$ are defined for each data point $x_i$ and its decompressed
    reconstruction $\hat{x}_i$, i.e. $R(x_i, \hat{x}_i)$.
    See the [`AnyRequirement`][....combinators.AnyRequirement] for more
    information.

    Parameters
    ----------
    value : int | float
        The non-negative and finite mean range-relative error bound.
    """

    kind: ClassVar[RequirementKind] = RequirementKind.mean_range_relative_error_bound
    value: int | float

    @override
    @classmethod
    def from_config(  # type: ignore
        cls,
        *,
        value: int | float,
    ) -> Self:
        """
        Construct the mean range-relative error bound requirement from its configuration.

        Parameters
        ----------
        value : int | float
            The non-negative and finite mean range-relative error bound.

        Returns
        -------
        requirement : Self
            The instantiated mean range-relative error bound requirement.
        """

        return cls(value=_parse_number(value))

    @override
    def get_config(self) -> Mapping[str, JSON]:
        """
        Get the configuration of this mean range-relative error bound requirement.

        Returns
        -------
        config : Mapping[str, JSON]
            Configuration in JSON object format.
        """

        return dict(kind=type(self).kind.get_config(), value=self.value)

    @override
    def humanise(self, *, format: Format | LiteralFormat = Format.plain) -> str:
        """
        Humanise the representation of this mean range-relative error bound requirement.

        Parameters
        ----------
        format : Format | LiteralFormat
            The format of the humanised representation.

        Returns
        -------
        humanised : str
            The humanised representation of this mean range-relative error
            bound requirement.
        """

        return f"{_humanise_kinded_type(self, format=format)}({self.value})"
