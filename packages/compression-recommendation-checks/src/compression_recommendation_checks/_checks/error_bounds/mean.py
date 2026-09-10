from fractions import Fraction

import numpy as np

from ..._compat import (
    _abs,
    _abs_fraction,
    _assign_or,
    _equal,
    _full,
    _isfinite,
    _isinf,
    _isnan,
    _logical_and,
    _multiply_fraction,
    _subtract_fraction,
    _sum_fraction,
)
from ..._convert import _array_to_finite_fractions_or_zero, _to_float
from ..._typing import _F_co
from ...typing import S_co, T_co
from . import _check_error_bound

__all__ = [
    "_check_mean_absolute_error_bound",
    "_check_mean_relative_error_bound",
    "_check_mean_range_relative_error_bound",
]


def _check_mean_absolute_error_bound(
    *,
    original: np.ndarray[S_co, np.dtype[T_co]],
    reconstructed: np.ndarray[S_co, np.dtype[T_co]],
    eb_mean_abs: int | float,
    ftype: np.dtype[_F_co],
) -> np.ndarray[S_co, np.dtype[np.bool]]:
    # PRE: ftype is chosen correctly

    # lossless conversion, assuming PRE
    original_float = _to_float(original, ftype)
    reconstructed_float = _to_float(reconstructed, ftype)

    isfinite = _isfinite(original)

    err_sum = _sum_fraction(
        _abs_fraction(
            _subtract_fraction(
                _array_to_finite_fractions_or_zero(original_float),
                _array_to_finite_fractions_or_zero(reconstructed_float),
            )
        ),
        where=isfinite,
    )

    bound_sum = _check_error_bound(eb_mean_abs) * Fraction(
        int(np.count_nonzero(isfinite))
    )

    ok: np.ndarray[S_co, np.dtype[np.bool]] = _full(
        original.shape, err_sum <= bound_sum
    )
    ok = _equal(original, reconstructed, out=ok, where=_isinf(original))
    ok = _isnan(reconstructed, out=ok, where=_isnan(original))

    return ok


def _check_mean_relative_error_bound(
    *,
    original: np.ndarray[S_co, np.dtype[T_co]],
    reconstructed: np.ndarray[S_co, np.dtype[T_co]],
    eb_mean_rel: int | float,
    ftype: np.dtype[_F_co],
) -> np.ndarray[S_co, np.dtype[np.bool]]:
    # PRE: ftype is chosen correctly

    # lossless conversion, assuming PRE
    original_float = _to_float(original, ftype)
    reconstructed_float = _to_float(reconstructed, ftype)

    isfinite = _isfinite(original)

    err_sum = _sum_fraction(
        _abs_fraction(
            _subtract_fraction(
                _array_to_finite_fractions_or_zero(original_float),
                _array_to_finite_fractions_or_zero(reconstructed_float),
            )
        ),
        where=isfinite,
    )

    bound_sum = _sum_fraction(
        _multiply_fraction(
            _array_to_finite_fractions_or_zero(_abs(original_float)),
            _check_error_bound(eb_mean_rel),
        ),
        where=isfinite,
    )

    ok: np.ndarray[S_co, np.dtype[np.bool]] = _full(
        original.shape, err_sum <= bound_sum
    )
    ok = _equal(original, reconstructed, out=ok, where=_isinf(original))
    ok = _isnan(reconstructed, out=ok, where=_isnan(original))
    ok = _equal(
        reconstructed,
        original.dtype.type(0),
        out=ok,
        where=_equal(original, original.dtype.type(0)),
    )

    return ok


def _check_mean_range_relative_error_bound(
    *,
    original: np.ndarray[S_co, np.dtype[T_co]],
    reconstructed: np.ndarray[S_co, np.dtype[T_co]],
    eb_mean_range_rel: int | float,
    ftype: np.dtype[_F_co],
) -> np.ndarray[S_co, np.dtype[np.bool]]:
    # PRE: ftype is chosen correctly

    # lossless conversion, assuming PRE
    original_float = _to_float(original, ftype)
    reconstructed_float = _to_float(reconstructed, ftype)

    is_finite = _isfinite(original)

    ok: np.ndarray[S_co, np.dtype[np.bool]]

    if not np.any(is_finite):
        ok = _equal(original, reconstructed)
        _assign_or(ok, _logical_and(_isnan(original), _isnan(reconstructed)))

        return ok

    # FIXME: $x_min and $x_max use non-NaN, here we use finite
    finite_min: _F_co = np.amin(
        original_float, where=is_finite, initial=ftype.type(np.inf)
    )
    finite_max: _F_co = np.amax(
        original_float, where=is_finite, initial=ftype.type(-np.inf)
    )

    range_fraction = Fraction(float(finite_max)) - Fraction(float(finite_min))

    err_sum = _sum_fraction(
        _abs_fraction(
            _subtract_fraction(
                _array_to_finite_fractions_or_zero(original_float),
                _array_to_finite_fractions_or_zero(reconstructed_float),
            )
        ),
        where=is_finite,
    )

    bound_sum = (
        _check_error_bound(eb_mean_range_rel)
        * range_fraction
        * Fraction(int(np.count_nonzero(is_finite)))
    )

    ok = _full(original.shape, err_sum <= bound_sum)
    ok = _equal(original, reconstructed, out=ok, where=_isinf(original))
    ok = _isnan(reconstructed, out=ok, where=_isnan(original))

    return ok
