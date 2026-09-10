import math
from fractions import Fraction

import numpy as np

from ..._compat import (
    _abs,
    _abs_fraction,
    _assign_or,
    _divide_fraction,
    _equal,
    _isfinite,
    _isnan,
    _less_equal_fraction,
    _logical_and,
    _multiply_fraction,
    _rsubtract_fraction,
    _subtract_fraction,
)
from ..._convert import _array_to_finite_fractions_or_zero, _to_float
from ..._typing import _F_co
from ...typing import S_co, T_co
from . import _check_error_bound

__all__ = [
    "_check_maximum_pointwise_absolute_error_bound",
    "_check_maximum_pointwise_relative_error_bound",
    "_check_maximum_pointwise_range_relative_error_bound",
    "_check_maximum_pointwise_quadratic_error_bound",
]


def _check_maximum_pointwise_absolute_error_bound(
    *,
    original: np.ndarray[S_co, np.dtype[T_co]],
    reconstructed: np.ndarray[S_co, np.dtype[T_co]],
    eb_abs: int | float,
    ftype: np.dtype[_F_co],
) -> np.ndarray[S_co, np.dtype[np.bool]]:
    # PRE: ftype is chosen correctly

    # lossless conversion, assuming PRE
    original_float = _to_float(original, ftype)
    reconstructed_float = _to_float(reconstructed, ftype)

    err = _abs_fraction(
        _subtract_fraction(
            _array_to_finite_fractions_or_zero(original_float),
            _array_to_finite_fractions_or_zero(reconstructed_float),
        )
    )

    bound = _check_error_bound(eb_abs)

    ok: np.ndarray[S_co, np.dtype[np.bool]] = _less_equal_fraction(err, bound)
    _assign_or(ok, _equal(original, reconstructed))
    _assign_or(ok, _logical_and(_isnan(original), _isnan(reconstructed)))

    return ok


def _check_maximum_pointwise_relative_error_bound(
    *,
    original: np.ndarray[S_co, np.dtype[T_co]],
    reconstructed: np.ndarray[S_co, np.dtype[T_co]],
    eb_rel: int | float,
    ftype: np.dtype[_F_co],
) -> np.ndarray[S_co, np.dtype[np.bool]]:
    # PRE: ftype is chosen correctly

    # lossless conversion, assuming PRE
    original_float = _to_float(original, ftype)
    reconstructed_float = _to_float(reconstructed, ftype)

    err = _abs_fraction(
        _subtract_fraction(
            _array_to_finite_fractions_or_zero(original_float),
            _array_to_finite_fractions_or_zero(reconstructed_float),
        )
    )

    bound = _multiply_fraction(
        _array_to_finite_fractions_or_zero(_abs(original_float)),
        _check_error_bound(eb_rel),
    )

    ok: np.ndarray[S_co, np.dtype[np.bool]] = _less_equal_fraction(err, bound)
    _assign_or(ok, _equal(original, reconstructed))
    _assign_or(ok, _logical_and(_isnan(original), _isnan(reconstructed)))

    return ok


def _check_maximum_pointwise_range_relative_error_bound(
    *,
    original: np.ndarray[S_co, np.dtype[T_co]],
    reconstructed: np.ndarray[S_co, np.dtype[T_co]],
    eb_range_rel: int | float,
    ftype: np.dtype[_F_co],
) -> np.ndarray[S_co, np.dtype[np.bool]]:
    # PRE: ftype is chosen correctly

    # lossless conversion, assuming PRE
    original_float = _to_float(original, ftype)
    reconstructed_float = _to_float(reconstructed, ftype)

    is_finite = _isfinite(original_float)

    ok: np.ndarray[S_co, np.dtype[np.bool]]

    if not np.any(is_finite):
        ok = _equal(original, reconstructed)
        _assign_or(ok, _logical_and(_isnan(original), _isnan(reconstructed)))

        return ok

    finite_min: _F_co = np.amin(
        original_float, where=is_finite, initial=ftype.type(np.inf)
    )
    finite_max: _F_co = np.amax(
        original_float, where=is_finite, initial=ftype.type(-np.inf)
    )

    range_fraction = Fraction(float(finite_max)) - Fraction(float(finite_min))

    err = _abs_fraction(
        _subtract_fraction(
            _array_to_finite_fractions_or_zero(original_float),
            _array_to_finite_fractions_or_zero(reconstructed_float),
        )
    )

    bound = _check_error_bound(eb_range_rel) * range_fraction

    ok = _less_equal_fraction(err, bound)
    _assign_or(ok, _equal(original, reconstructed))
    _assign_or(ok, _logical_and(_isnan(original), _isnan(reconstructed)))

    return ok


def _check_maximum_pointwise_quadratic_error_bound(
    *,
    original: np.ndarray[S_co, np.dtype[T_co]],
    reconstructed: np.ndarray[S_co, np.dtype[T_co]],
    eb_qua: int | float,
    minimum: int | float,
    maximum: int | float,
    ftype: np.dtype[_F_co],
) -> np.ndarray[S_co, np.dtype[np.bool]]:
    # PRE: ftype is chosen correctly

    # lossless conversion, assuming PRE
    original_float = _to_float(original, ftype)
    reconstructed_float = _to_float(reconstructed, ftype)

    err = _abs_fraction(
        _subtract_fraction(
            _array_to_finite_fractions_or_zero(original_float),
            _array_to_finite_fractions_or_zero(reconstructed_float),
        )
    )

    if not math.isfinite(minimum):
        raise ValueError("minimum must be finite")
    if not math.isfinite(maximum):
        raise ValueError("maximum must be finite")

    minimum_fraction = Fraction(minimum)
    maximum_fraction = Fraction(maximum)
    range_fraction = maximum_fraction - minimum_fraction

    if range_fraction < 0:
        raise ValueError("maximum must be greater than or equal to minimum")

    ok: np.ndarray[S_co, np.dtype[np.bool]]

    if range_fraction == 0:
        ok = _equal(original, reconstructed)
        _assign_or(ok, _logical_and(_isnan(original), _isnan(reconstructed)))

        return ok

    original_norm = _subtract_fraction(
        _multiply_fraction(
            _divide_fraction(
                _subtract_fraction(
                    _array_to_finite_fractions_or_zero(_abs(original_float)),
                    minimum_fraction,
                ),
                range_fraction,
            ),
            Fraction(2),
        ),
        Fraction(1),
    )

    bound = _multiply_fraction(
        _rsubtract_fraction(
            Fraction(1), _multiply_fraction(original_norm, original_norm)
        ),
        _check_error_bound(eb_qua),
    )

    ok = _less_equal_fraction(err, bound)
    _assign_or(ok, _equal(original, reconstructed))
    _assign_or(ok, _logical_and(_isnan(original), _isnan(reconstructed)))

    return ok
