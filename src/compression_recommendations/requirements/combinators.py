"""
Logical combinations of multiple requirements.
"""

from collections.abc import Collection, Mapping
from dataclasses import dataclass
from typing import ClassVar, Literal, Self

from typing_extensions import override  # MSPV 3.12

from ..typing import JSON
from .abc import Requirement
from .kind import RequirementKind

__all__ = ["AnyRequirement", "AllRequirements"]


@dataclass(kw_only=True, slots=True)
class AnyRequirement(Requirement):
    r"""
    Require that at least one of the sub-`requirements` is fulfilled.

    \[
    R_{\text{any}(\{ R_0, \ldots, R_J \})}(x_i, \hat{x}_i)
        := \exists j \mathbin{.} R_j(x_i, \hat{x}_i)
    \]

    Requirements $R$ are defined for each data point $x_i$ and its decompressed
    reconstruction $\hat{x}_i$, i.e. $R(x_i, \hat{x}_i)$.

    For each data point, at least one of the sub-`requirements`
    $R_j(x_i, \hat{x_i})$ must be fulfilled for the any-requirement to be
    fulfilled, allowing pointwise requirements to compose naturally.

    For non-pointwise requirements, each point $x_i$ effectively requires the
    non-pointwise requirement to be fulfilled over all points related to $x_i$.
    For global requirements, each point $x_i$ thus requires the global
    requirement to be fulfilled, i.e.
    $R(x_i, \hat{x}_i) = R_{global}(x, \hat{x})$.
    """

    kind: ClassVar[RequirementKind] = RequirementKind.any
    requirements: Collection[Requirement]

    @override
    @classmethod
    def from_config(  # type: ignore
        cls,
        *,
        requirements: Collection[Mapping[str, JSON]],
        kind: Literal["any"] = RequirementKind.any.value,
    ) -> Self:
        return cls(
            requirements=tuple(
                Requirement.from_config(
                    **requirement  # type: ignore
                )
                for requirement in requirements
            )
        )

    @override
    def get_config(self) -> Mapping[str, JSON]:
        return dict(
            kind=type(self).kind.get_config(),
            requirements=[
                requirement.get_config() for requirement in self.requirements
            ],
        )

    @override
    def humanise(self) -> str:
        match self.requirements:
            case ():
                return "False"
            case (requirement,):
                return requirement.humanise()
            case requirements:
                return f"({' or '.join(requirement.humanise() for requirement in requirements)})"


@dataclass(kw_only=True, slots=True)
class AllRequirements(Requirement):
    r"""
    Require that all of the sub-`requirements` are fulfilled.

    \[
    R_{\text{all}(\{ R_0, \ldots, R_J \})}(x_i, \hat{x}_i)
        := \forall j \mathbin{.} R_j(x_i, \hat{x}_i)
    \]

    Requirements $R$ are defined for each data point $x_i$ and its decompressed
    reconstruction $\hat{x}_i$, i.e. $R(x_i, \hat{x}_i)$.
    See the [`AnyRequirement`][..AnyRequirement] for more information.
    """

    kind: ClassVar[RequirementKind] = RequirementKind.all
    requirements: Collection[Requirement]

    @override
    @classmethod
    def from_config(  # type: ignore
        cls,
        *,
        requirements: Collection[Mapping[str, JSON]],
        kind: Literal["all"] = RequirementKind.all.value,
    ) -> Self:
        return cls(
            requirements=tuple(
                Requirement.from_config(
                    **requirement  # type: ignore
                )
                for requirement in requirements
            )
        )

    @override
    def get_config(self) -> Mapping[str, JSON]:
        return dict(
            kind=type(self).kind.get_config(),
            requirements=[
                requirement.get_config() for requirement in self.requirements
            ],
        )

    @override
    def humanise(self) -> str:
        match self.requirements:
            case ():
                return "True"
            case (requirement,):
                return requirement.humanise()
            case requirements:
                return f"({' and '.join(requirement.humanise() for requirement in requirements)})"
