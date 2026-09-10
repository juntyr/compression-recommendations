"""
Data limit-preserving requirements.
"""

import math
from collections.abc import Mapping
from dataclasses import dataclass
from typing import ClassVar, Self, assert_never

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

    The limits must not be NaN.

    If an original data value $x_i$ is not within the limits, no requirement is
    imposed on the decompressed data value $\hat{x}_i$.

    Requirements $R$ are defined for each data point $x_i$ and its decompressed
    reconstruction $\hat{x}_i$, i.e. $R(x_i, \hat{x}_i)$.
    See the [`AnyRequirement`][...combinators.AnyRequirement] for more
    information.

    Parameters
    ----------
    minimum : None | int | float
        The optional lower data limit to preserve.
    maximum : None | int | float
        The optional upper data limit to preserve.
    """

    kind: ClassVar[RequirementKind] = RequirementKind.data_limits
    minimum: None | int | float = None
    maximum: None | int | float = None

    def __init__(
        self, *, minimum: None | int | float = None, maximum: None | int | float = None
    ) -> None:
        if minimum is not None and math.isnan(minimum):
            raise ValueError("minimum must not be NaN")
        if maximum is not None and math.isnan(maximum):
            raise ValueError("maximum must not be NaN")
        if (minimum is not None) and (maximum is not None) and (maximum < minimum):
            raise ValueError("maximum must be greater than or equal to minimum")

        self.minimum = minimum
        self.maximum = maximum

    @override
    @classmethod
    def from_config(  # type: ignore
        cls,
        *,
        minimum: None | int | float = None,
        maximum: None | int | float = None,
    ) -> Self:
        """
        Construct the data limits requirement from its configuration.

        Parameters
        ----------
        minimum : None | int | float
            The optional lower data limit to preserve.
        maximum : None | int | float
            The optional upper data limit to preserve.

        Returns
        -------
        requirement : Self
            The instantiated data limits requirement.
        """

        return cls(
            minimum=None if minimum is None else _parse_number(minimum),
            maximum=None if maximum is None else _parse_number(maximum),
        )

    @override
    def get_config(self) -> Mapping[str, JSON]:
        """
        Get the configuration of this data limits requirement.

        Returns
        -------
        config : Mapping[str, JSON]
            Configuration in JSON object format.
        """

        config: dict[str, JSON] = dict(kind=type(self).kind.get_config())
        if self.minimum is not None:
            config["minimum"] = self.minimum
        if self.maximum is not None:
            config["maximum"] = self.maximum
        return config

    @override
    def humanise(self, *, format: Format | LiteralFormat = Format.plain) -> str:
        """
        Humanise the representation of this data limits requirement.

        Parameters
        ----------
        format : Format | LiteralFormat
            The format of the humanised representation.

        Returns
        -------
        humanised : str
            The humanised representation of this data limits requirement.
        """

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
