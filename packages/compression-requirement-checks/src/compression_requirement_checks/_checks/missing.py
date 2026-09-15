import math
from fractions import Fraction

import numpy as np

from .._compat import _equal, _equal_bool, _isnan, _true
from .._convert import _fraction_to_float_exact, _to_float
from .._typing import _F_co
from ..typing import S_co, T_co

__all__ = ["_check_missing_value"]


def _check_missing_value(
    *,
    original: np.ndarray[S_co, np.dtype[T_co]],
    reconstructed: np.ndarray[S_co, np.dtype[T_co]],
    missing_value: int | float,
    ftype: np.dtype[_F_co],
) -> np.ndarray[S_co, np.dtype[np.bool]]:
    # PRE: ftype is chosen correctly

    # lossless conversion, assuming PRE
    original_float = _to_float(original, ftype)
    reconstructed_float = _to_float(reconstructed, ftype)

    if math.isnan(missing_value):
        return _equal_bool(_isnan(original), _isnan(reconstructed))

    missing_value_exact_float: _F_co

    if math.isfinite(missing_value):
        missing_value_fraction = Fraction(missing_value)
        # lossless conversion
        missing_value_exact_float_ = _fraction_to_float_exact(
            missing_value_fraction, ftype
        )

        if missing_value_exact_float_ is None:
            return _true(original.shape)

        missing_value_exact_float = missing_value_exact_float_
    else:
        # exact conversion
        missing_value_exact_float = ftype.type(missing_value)

    return _equal_bool(
        _equal(original_float, missing_value_exact_float),
        _equal(reconstructed_float, missing_value_exact_float),
    )
