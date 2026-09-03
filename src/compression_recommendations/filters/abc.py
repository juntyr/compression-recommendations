"""
Abstract base class for filters.
"""

from abc import ABC, abstractmethod
from collections.abc import Mapping
from typing import ClassVar, Self

from typing_extensions import override  # MSPV 3.12

from ..config import Config
from ..typing import JSON
from .kind import FilterKind

__all__ = ["Filter"]


class Filter(Config, ABC):
    """
    Abstract base class for filters, which decide which [`Requirement`][compression_recommendations.requirements.abc.Requirement]s apply.
    """

    __slots__: tuple[str, ...] = ()

    kind: ClassVar[FilterKind]

    @abstractmethod
    def matches(
        self, *, markers: Mapping[str, None | bool | int | float | str]
    ) -> bool:
        """
        Check if the `markers` match this filter.

        Please refer to the individual filter implementations, or use their
        `Filter.markers_for` method, to see which markers they match.

        Parameters
        ----------
        markers : Mapping[str, None | bool | int | float | str]
            The markers that identify the use case, e.g. the variable.

        Returns
        -------
        matches : bool
            [`True`][True] if the `markers` match, [`False`][False] otherwise.
        """

    @override
    @classmethod
    def from_config(cls, *, kind: str, **kwargs: JSON) -> Self:  # type: ignore
        """
        Construct the specific filter from its `kind` and [`JSON`][compression_recommendations.typing.JSON] configuration.

        Parameters
        ----------
        kind : str
            The filter kind.
        **kwargs : JSON
            The filter configuration.

        Returns
        -------
        filter : Self
            The instantiated filter.
        """

        return FilterKind.from_config(kind=kind).cls.from_config(
            **kwargs  # type: ignore
        )
