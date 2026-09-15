import math
from fractions import Fraction

import numpy as np

from .._compat import _equal, _greater, _less, _true
from .._convert import (
    _fraction_to_float_exact,
    _fraction_to_float_round_ties_down,
    _fraction_to_float_round_ties_up,
    _to_float,
)
from .._typing import _F_co
from ..typing import S_co, T_co

__all__ = ["_check_isovalue"]


def _check_isovalue(
    *,
    original: np.ndarray[S_co, np.dtype[T_co]],
    reconstructed: np.ndarray[S_co, np.dtype[T_co]],
    isovalue: int | float,
    ftype: np.dtype[_F_co],
) -> np.ndarray[S_co, np.dtype[np.bool]]:
    # PRE: ftype is chosen correctly

    # lossless conversion, assuming PRE
    original_float = _to_float(original, ftype)
    reconstructed_float = _to_float(reconstructed, ftype)

    isovalue_exact_float: None | _F_co
    isovalue_ties_up_float: None | _F_co
    isovalue_ties_down_float: None | _F_co

    if math.isfinite(isovalue):
        isovalue_fraction = Fraction(isovalue)
        # lossless conversion
        isovalue_exact_float = _fraction_to_float_exact(isovalue_fraction, ftype)
        # conservative conversions
        isovalue_ties_up_float = _fraction_to_float_round_ties_up(
            isovalue_fraction, ftype
        )
        isovalue_ties_down_float = _fraction_to_float_round_ties_down(
            isovalue_fraction, ftype
        )
    elif math.isnan(isovalue):
        isovalue_exact_float = isovalue_ties_up_float = isovalue_ties_down_float = None
    else:
        # exact conversion
        isovalue_exact_float = isovalue_ties_up_float = isovalue_ties_down_float = (
            ftype.type(isovalue)
        )

    ok: np.ndarray[S_co, np.dtype[np.bool]] = _true(original.shape)

    if isovalue_ties_up_float is not None:
        _less(
            reconstructed_float,
            isovalue_ties_up_float,
            out=ok,
            where=_less(original_float, isovalue_ties_up_float),
        )

    if isovalue_exact_float is not None:
        _equal(
            reconstructed_float,
            isovalue_exact_float,
            out=ok,
            where=_equal(original_float, isovalue_exact_float),
        )

    if isovalue_ties_down_float is not None:
        _greater(
            reconstructed_float,
            isovalue_ties_down_float,
            out=ok,
            where=_greater(original_float, isovalue_ties_down_float),
        )

    return ok
