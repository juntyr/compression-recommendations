"""
Abstract base class for requirements.
"""

from abc import ABC
from typing import ClassVar, Self

from typing_extensions import override  # MSPV 3.12

from ..config import Config
from ..typing import JSON
from .kind import RequirementKind

__all__ = ["Requirement"]


class Requirement(Config, ABC):
    """
    Abstract base class for requirements, which define the safety requirements that lossy compression must uphold.
    """

    __slots__: tuple[str, ...] = ()

    kind: ClassVar[RequirementKind]

    @override
    @classmethod
    def from_config(cls, *, kind: str, **kwargs: JSON) -> Self:  # type: ignore
        """
        Construct the specific requirement from its `kind` and [`JSON`][compression_recommendations.typing.JSON] configuration.

        Parameters
        ----------
        kind : str
            The requirement kind.
        **kwargs : JSON
            The requirement configuration.

        Returns
        -------
        requirement : Self
            The instantiated requirement.
        """

        return RequirementKind.from_config(kind).cls.from_config(
            **kwargs  # type: ignore
        )
