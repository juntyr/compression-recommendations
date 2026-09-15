import math
from fractions import Fraction

import numpy as np

from .._compat import _greater_equal, _less_equal, _logical_and, _true
from .._convert import (
    _fraction_to_float_round_ties_down,
    _fraction_to_float_round_ties_up,
    _to_float,
)
from .._typing import _F_co
from ..typing import S_co, T_co

__all__ = ["_check_data_limits"]


def _check_data_limits(
    *,
    original: np.ndarray[S_co, np.dtype[T_co]],
    reconstructed: np.ndarray[S_co, np.dtype[T_co]],
    minimum: None | int | float,
    maximum: None | int | float,
    ftype: np.dtype[_F_co],
) -> np.ndarray[S_co, np.dtype[np.bool]]:
    # PRE: ftype is chosen correctly

    # lossless conversion, assuming PRE
    original_float = _to_float(original, ftype)
    reconstructed_float = _to_float(reconstructed, ftype)

    ok: np.ndarray[S_co, np.dtype[np.bool]] = _true(original.shape)

    minimum_float: None | _F_co
    maximum_float: None | _F_co

    if minimum is None:
        minimum_float = None
    else:
        if math.isnan(minimum):
            raise ValueError("minimum must not be NaN")

        # conservative conversion
        if math.isinf(minimum):
            minimum_float = ftype.type(minimum)
        else:
            minimum_float = _fraction_to_float_round_ties_up(Fraction(minimum), ftype)

    if maximum is None:
        maximum_float = None
    else:
        if math.isnan(maximum):
            raise ValueError("maximum must not be NaN")

        # conservative conversion
        if math.isinf(maximum):
            maximum_float = ftype.type(maximum)
        else:
            maximum_float = _fraction_to_float_round_ties_down(Fraction(maximum), ftype)

    match (minimum_float, maximum_float):
        case (None, None):
            pass
        case (minimum_float, None):
            assert minimum_float is not None  # TODO: remove
            ok = _logical_and(
                ok,
                _greater_equal(reconstructed_float, minimum_float),
                out=ok,
                where=_greater_equal(original_float, minimum_float),
            )
        case (None, maximum_float):
            assert maximum_float is not None  # TODO: remove
            ok = _logical_and(
                ok,
                _less_equal(reconstructed_float, maximum_float),
                out=ok,
                where=_less_equal(original_float, maximum_float),
            )
        case (minimum_float, maximum_float):
            ok = _logical_and(
                ok,
                _logical_and(
                    _greater_equal(reconstructed_float, minimum_float),
                    _less_equal(reconstructed_float, maximum_float),
                ),
                out=ok,
                where=_logical_and(
                    _greater_equal(original_float, minimum_float),
                    _less_equal(original_float, maximum_float),
                ),
            )

    return ok
