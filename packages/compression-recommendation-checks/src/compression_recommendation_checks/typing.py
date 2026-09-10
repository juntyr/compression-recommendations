"""
Commonly used type variables and type aliases.
"""

from typing import TypeVar

import numpy as np

__all__ = ["F_co", "S_in", "S_co", "T_co"]

F_co = TypeVar("F_co", bound=np.floating, covariant=True)
""" Any numpy [`floating`][numpy.floating]-point data type (covariant). """

S_in = TypeVar("S_in", bound=tuple[int, ...])
""" Any array shape (invariant). """

S_co = TypeVar("S_co", bound=tuple[int, ...], covariant=True)
""" Any array shape (covariant). """

T_co = TypeVar("T_co", bound=np.number, covariant=True)
""" Any numpy [`number`][numpy.number] data type (covariant). """
