import numpy as np

from .._compat import _equal
from .._convert import _as_bits
from ..typing import S_co, T_co

__all__ = ["_check_lossless"]


def _check_lossless(
    *,
    original: np.ndarray[S_co, np.dtype[T_co]],
    reconstructed: np.ndarray[S_co, np.dtype[T_co]],
) -> np.ndarray[S_co, np.dtype[np.bool]]:
    return _equal(_as_bits(original), _as_bits(reconstructed))
