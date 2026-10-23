"""
Isovalue-preserving requirements.
"""

import math
from collections.abc import Mapping
from dataclasses import dataclass
from typing import ClassVar, Self

import strictyaml
from typing_extensions import override  # MSPV 3.12

from ..config import Format, LiteralFormat, _humanise_kinded_type
from ..typing import JSON
from .abc import Requirement
from .kind import RequirementKind

__all__ = ["IsovalueRequirement"]


@dataclass(kw_only=True, slots=True)
class IsovalueRequirement(Requirement):
    r"""
    Require that the iso`value` is preserved.

    \[
    \begin{align*}
    R_{\text{isovalue}(v)}(x_i, \hat{x}_i) &:= ((\hat{x}_i < v) \iff (x_i < v)) \\
        &\land ((\hat{x}_i = v) \iff (x_i = v)) \\
        &\land ((\hat{x}_i > v) \iff (x_i > v))
    \end{align*}
    \]

    The isovalue must not be NaN, use a
    [`MissingValueRequirement`][...missing.MissingValueRequirement] instead.

    Requirements $R$ are defined for each data point $x_i$ and its decompressed
    reconstruction $\hat{x}_i$, i.e. $R(x_i, \hat{x}_i)$.
    See the [`AnyRequirement`][...combinators.AnyRequirement] for more
    information.

    Parameters
    ----------
    value : int | float
        The isovalue to preserve.
    """

    kind: ClassVar[RequirementKind] = RequirementKind.isovalue
    value: int | float

    def __init__(self, *, value: int | float) -> None:
        if math.isnan(value):
            raise ValueError("value must not be NaN")

        self.value = value

    @override
    @classmethod
    def from_config(  # type: ignore
        cls,
        *,
        value: int | float,
    ) -> Self:
        """
        Construct the isovalue requirement from its configuration.

        Parameters
        ----------
        value : int | float
            The isovalue to preserve.

        Returns
        -------
        requirement : Self
            The instantiated isovalue requirement.
        """

        return cls(value=value)

    @override
    def get_config(self) -> Mapping[str, JSON]:
        """
        Get the configuration of this isovalue requirement.

        Returns
        -------
        config : Mapping[str, JSON]
            Configuration in JSON object format.
        """

        return dict(kind=type(self).kind.get_config(), value=self.value)

    @override
    def humanise(self, *, format: Format | LiteralFormat = Format.plain) -> str:
        """
        Humanise the representation of this isovalue requirement.

        Parameters
        ----------
        format : Format | LiteralFormat
            The format of the humanised representation.

        Returns
        -------
        humanised : str
            The humanised representation of this isovalue requirement.
        """

        return f"{_humanise_kinded_type(self, format=format)}({self.value})"

    @override
    @classmethod
    def _schema(cls) -> strictyaml.Validator:
        return strictyaml.Map(
            {
                "kind": strictyaml.Enum([cls.kind.value]),
                "value": strictyaml.Int() | strictyaml.Float(),
            }
        )
