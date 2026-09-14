"""
# Check Safety requirements for Safe Lossy Compression of weather and climate data

This package allows checking whether lossy compression, or any other data
reconstruction procedure, meets compression safety
[`Requirement`][compression_recommendations.requirements.abc.Requirement]s.
"""

from collections.abc import Collection

import numpy as np
from compression_recommendations.requirements.abc import Requirement

from ._checks import _check_safety_requirement_pointwise
from .typing import S_co, T_co

__all__ = ["check_safety_requirements", "check_safety_requirement"]


def check_safety_requirements(
    *,
    original: np.ndarray[S_co, np.dtype[T_co]],
    reconstructed: np.ndarray[S_co, np.dtype[T_co]],
    requirements: Collection[Requirement],
) -> bool:
    """
    Check whether all of the safety `requirements` are met by the `reconstructed` data with respect to the `original` data.

    Parameters
    ----------
    original : np.ndarray[S_co, np.dtype[T_co]]
        The original, uncompressed data.
    reconstructed : np.ndarray[S_co, np.dtype[T_co]]
        The reconstructed, decompressed data.
    requirements : Collection[Requirement]
        The safety requirements to check.

    Returns
    -------
    ok : bool
        Returns [`True`][True] if all safety `requirements` were met, and
        [`False`][False] otherwise.
    """

    return all(
        check_safety_requirement(
            original=original, reconstructed=reconstructed, requirement=requirement
        )
        for requirement in requirements
    )


def check_safety_requirement(
    *,
    original: np.ndarray[S_co, np.dtype[T_co]],
    reconstructed: np.ndarray[S_co, np.dtype[T_co]],
    requirement: Requirement,
) -> bool:
    """
    Check whether the safety `requirement` is met by the `reconstructed` data with respect to the `original` data.

    Parameters
    ----------
    original : np.ndarray[S_co, np.dtype[T_co]]
        The original, uncompressed data.
    reconstructed : np.ndarray[S_co, np.dtype[T_co]]
        The reconstructed, decompressed data.
    requirement : Requirement
        The safety requirement to check.

    Returns
    -------
    ok : bool
        Returns [`True`][True] if the safety `requirement` was met, and
        [`False`][False] otherwise.
    """

    if original.dtype != reconstructed.dtype:
        raise TypeError(
            f"original and reconstructed dtype must match: {original.dtype.name} vs {reconstructed.dtype.name}"
        )
    if original.shape != reconstructed.shape:
        raise TypeError(
            f"original and reconstructed shape must match: {original.shape} vs {reconstructed.shape}"
        )

    return bool(
        np.all(
            _check_safety_requirement_pointwise(
                original=original, reconstructed=reconstructed, requirement=requirement
            )
        )
    )
