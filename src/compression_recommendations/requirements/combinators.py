"""
Logical combinations of multiple requirements.
"""

from collections.abc import Collection, Mapping
from dataclasses import dataclass
from typing import ClassVar, Self

from typing_extensions import override  # MSPV 3.12

from ..config import Format, LiteralFormat, _humanise_labelled_type
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

    Parameters
    ----------
    requirements : Collection[Requirement]
        The sub-requirements for this any-requirement combinator.
    """

    kind: ClassVar[RequirementKind] = RequirementKind.any
    requirements: Collection[Requirement]

    @override
    @classmethod
    def from_config(  # type: ignore
        cls,
        *,
        requirements: Collection[Mapping[str, JSON]],
    ) -> Self:
        """
        Construct the any-requirement combinator from its configuration.

        Parameters
        ----------
        requirements : Collection[Mapping[str, JSON]]
            The configuration for the sub-requirements for this
            any-requirement combinator.

        Returns
        -------
        requirement : Self
            The instantiated any-requirement combinator.
        """

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
        """
        Get the configuration of this any-requirement combinator.

        Returns
        -------
        config : Mapping[str, JSON]
            Configuration in JSON object format.
        """

        return dict(
            kind=type(self).kind.get_config(),
            requirements=[
                requirement.get_config() for requirement in self.requirements
            ],
        )

    @override
    def humanise(self, *, format: Format | LiteralFormat = Format.plain) -> str:
        """
        Humanise the representation of this any-requirement combinator.

        Parameters
        ----------
        format : Format | LiteralFormat
            The format of the humanised representation.

        Returns
        -------
        humanised : str
            The humanised representation of this any-requirement combinator.
        """

        match self.requirements:
            case ():
                return _humanise_labelled_type(self, label="False", format=format)
            case (requirement,):
                return requirement.humanise(format=format)
            case requirements:
                or_ = _humanise_labelled_type(self, label="or", format=format)
                return f"({f' {or_} '.join(requirement.humanise(format=format) for requirement in requirements)})"


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

    Parameters
    ----------
    requirements : Collection[Requirement]
        The sub-requirements for this all-requirements combinator.
    """

    kind: ClassVar[RequirementKind] = RequirementKind.all
    requirements: Collection[Requirement]

    @override
    @classmethod
    def from_config(  # type: ignore
        cls,
        *,
        requirements: Collection[Mapping[str, JSON]],
    ) -> Self:
        """
        Construct the all-requirements combinator from its configuration.

        Parameters
        ----------
        requirements : Collection[Mapping[str, JSON]]
            The configuration for the sub-requirements for this
            all-requirements combinator.

        Returns
        -------
        requirement : Self
            The instantiated all-requirements combinator.
        """

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
        """
        Get the configuration of this all-requirements combinator.

        Returns
        -------
        config : Mapping[str, JSON]
            Configuration in JSON object format.
        """

        return dict(
            kind=type(self).kind.get_config(),
            requirements=[
                requirement.get_config() for requirement in self.requirements
            ],
        )

    @override
    def humanise(self, *, format: Format | LiteralFormat = Format.plain) -> str:
        """
        Humanise the representation of this all-requirements combinator.

        Parameters
        ----------
        format : Format | LiteralFormat
            The format of the humanised representation.

        Returns
        -------
        humanised : str
            The humanised representation of this all-requirements combinator.
        """

        match self.requirements:
            case ():
                return _humanise_labelled_type(self, label="True", format=format)
            case (requirement,):
                return requirement.humanise(format=format)
            case requirements:
                and_ = _humanise_labelled_type(self, label="and", format=format)
                return f"({f' {and_} '.join(requirement.humanise(format=format) for requirement in requirements)})"
