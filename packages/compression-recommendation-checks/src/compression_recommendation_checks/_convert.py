from fractions import Fraction
from typing import TypeGuard

import numpy as np

from ._compat import _extract_scalar, _to_finite_or_zero
from ._typing import _F_co, _Fraction
from .typing import S_co, T_co

__all__ = [
    "_as_bits",
    "_as_fraction",
    "_array_to_finite_fractions_or_zero",
    "_fraction_to_float_exact",
    "_fraction_to_float_round_ties_down",
    "_fraction_to_float_round_ties_up",
    "_is_of_dtype",
    "_get_lossless_floating_point_type",
    "_to_float",
]


def _as_bits(
    a: np.ndarray[S_co, np.dtype[T_co]],
) -> np.ndarray[S_co, np.dtype[np.unsignedinteger]]:
    return a.view(a.dtype.str.replace("f", "u").replace("i", "u"))


@np.vectorize(otypes=[Fraction], signature="()->()")
def _as_fraction_(x: np.float16 | np.float32 | np.float64) -> Fraction:
    return Fraction(float(x))


def _as_fraction(
    x: np.ndarray[S_co, np.dtype[_F_co]],
    *,
    out: None | np.ndarray[S_co, np.dtype[_Fraction]] = None,
    where: None | np.ndarray[S_co, np.dtype[np.bool]] = None,
) -> np.ndarray[S_co, np.dtype[_Fraction]]:
    return _as_fraction_(x, out=out, where=where)  # type: ignore


def _array_to_finite_fractions_or_zero(
    x: np.ndarray[S_co, np.dtype[_F_co]],
) -> np.ndarray[S_co, np.dtype[_Fraction]]:
    assert x.dtype in (np.dtype(np.float16), np.dtype(np.float64), np.dtype(np.float64))

    return _as_fraction(_to_finite_or_zero(x))


def _fraction_to_float_exact(x: Fraction, ftype: np.dtype[_F_co]) -> None | _F_co:
    assert ftype in (np.dtype(np.float16), np.dtype(np.float64), np.dtype(np.float64))

    try:
        x_float = float(x)
    except OverflowError:
        return None

    x_f: _F_co = _extract_scalar(np.array(x_float).astype(ftype))

    # this is lossless since ftype <= float
    x_f_fraction = Fraction(float(x_f))

    if x_f_fraction == x:
        return x_f

    return None


def _fraction_to_float_round_ties_down(x: Fraction, ftype: np.dtype[_F_co]) -> _F_co:
    assert ftype in (np.dtype(np.float16), np.dtype(np.float64), np.dtype(np.float64))

    try:
        x_float = float(x)
    except OverflowError:
        return ftype.type(-np.inf) if x < 0 else np.finfo(ftype).max

    x_f: _F_co = _extract_scalar(np.array(x_float).astype(ftype))

    # this is lossless since ftype <= float
    x_f_fraction = Fraction(float(x_f))

    if x_f_fraction > x:
        x_f = np.nextafter(x_f, ftype.type(-np.inf))
        x_f_fraction = Fraction(float(x_f))

    assert x_f_fraction <= x

    return x_f


def _fraction_to_float_round_ties_up(x: Fraction, ftype: np.dtype[_F_co]) -> _F_co:
    assert ftype in (np.dtype(np.float16), np.dtype(np.float64), np.dtype(np.float64))

    try:
        x_float = float(x)
    except OverflowError:
        return np.finfo(ftype).min if x < 0 else ftype.type(np.inf)

    x_f: _F_co = _extract_scalar(np.array(x_float).astype(ftype))

    # this is lossless since ftype <= float
    x_f_fraction = Fraction(float(x_f))

    if x_f_fraction < x:
        x_f = np.nextafter(x_f, ftype.type(np.inf))
        x_f_fraction = Fraction(float(x_f))

    assert x_f_fraction >= x

    return x_f


# type guard for x.dtype == dtype
def _is_of_dtype(
    x: np.ndarray[S_co, np.dtype[np.number]], dtype: np.dtype[T_co]
) -> TypeGuard[np.ndarray[S_co, np.dtype[T_co]]]:
    return x.dtype == dtype


def _get_lossless_floating_point_type(
    dtype: np.dtype[np.number],
) -> np.dtype[np.float16 | np.float32 | np.float64]:
    SMALLEST_LOSSLESS_FTYPE: dict[
        np.dtype[np.number], np.dtype[np.float16 | np.float32 | np.float64]
    ] = {
        np.dtype(np.int8): np.dtype(np.float16),
        np.dtype(np.int16): np.dtype(np.float32),
        np.dtype(np.int32): np.dtype(np.float64),
        np.dtype(np.uint8): np.dtype(np.float16),
        np.dtype(np.uint16): np.dtype(np.float32),
        np.dtype(np.uint32): np.dtype(np.float64),
        np.dtype(np.float16): np.dtype(np.float16),
        np.dtype(np.float32): np.dtype(np.float32),
        np.dtype(np.float64): np.dtype(np.float64),
    }
    if dtype in SMALLEST_LOSSLESS_FTYPE:
        return SMALLEST_LOSSLESS_FTYPE[dtype]
    raise TypeError(f"unsupported data type {dtype.name}")


def _to_float(
    x: np.ndarray[S_co, np.dtype[T_co]], ftype: np.dtype[_F_co]
) -> np.ndarray[S_co, np.dtype[_F_co]]:
    assert ftype in (np.dtype(np.float16), np.dtype(np.float64), np.dtype(np.float64))

    if np.issubdtype(x.dtype, np.floating):
        assert ftype.itemsize >= x.dtype.itemsize
    else:
        assert np.finfo(ftype).nmant >= x.dtype.itemsize

    if _is_of_dtype(x, ftype):
        return x

    # lossless cast to floating-point data type with a sufficiently large
    #  mantissa
    return x.astype(ftype, casting="safe")
