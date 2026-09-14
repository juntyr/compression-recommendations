from fractions import Fraction
from typing import Literal

import numpy as np

from ._typing import _F_co, _Fraction
from .typing import S_co, S_in, T_co

__all__ = [
    "_abs",
    "_abs_fraction",
    "_assign_and",
    "_assign_or",
    "_divide_fraction",
    "_equal",
    "_equal_bool",
    "_extract_scalar",
    "_false",
    "_fraction_to_scalar",
    "_full",
    "_greater",
    "_greater_fraction",
    "_greater_equal",
    "_greater_equal_fraction",
    "_isfinite",
    "_isinf",
    "_isnan",
    "_less",
    "_less_fraction",
    "_less_equal",
    "_less_equal_fraction",
    "_logical_and",
    "_logical_or",
    "_multiply_fraction",
    "_nextafter",
    "_subtract",
    "_subtract_fraction",
    "_rsubtract_fraction",
    "_sum_fraction",
    "_to_finite_or_zero",
    "_true",
]


def _abs(
    x: np.ndarray[S_co, np.dtype[_F_co]],
) -> np.ndarray[S_co, np.dtype[_F_co]]:
    return np.abs(x)  # type: ignore


def _abs_fraction(
    x: np.ndarray[S_co, np.dtype[_Fraction]],
) -> np.ndarray[S_co, np.dtype[_Fraction]]:
    return np.abs(x)  # type: ignore


def _assign_and(
    out: np.ndarray[S_co, np.dtype[np.bool]], and_: np.ndarray[S_co, np.dtype[np.bool]]
) -> None:
    out &= and_


def _assign_or(
    out: np.ndarray[S_co, np.dtype[np.bool]], or_: np.ndarray[S_co, np.dtype[np.bool]]
) -> None:
    out |= or_


def _divide_fraction(
    x: np.ndarray[S_co, np.dtype[_Fraction]],
    y: Fraction | np.ndarray[S_co, np.dtype[_Fraction]],
) -> np.ndarray[S_co, np.dtype[_Fraction]]:
    return x / y  # type: ignore


def _equal(
    x: np.ndarray[S_co, np.dtype[T_co]],
    y: T_co | np.ndarray[S_co, np.dtype[T_co]],
    *,
    out: None | np.ndarray[S_co, np.dtype[np.bool]] = None,
    where: Literal[True] | np.ndarray[S_co, np.dtype[np.bool]] = True,
) -> np.ndarray[S_co, np.dtype[np.bool]]:
    return np.equal(x, y, out=out, where=where)  # type: ignore


def _equal_bool(
    x: np.ndarray[S_co, np.dtype[np.bool]], y: np.ndarray[S_co, np.dtype[np.bool]]
) -> np.ndarray[S_co, np.dtype[np.bool]]:
    return x == y  # type: ignore


def _extract_scalar(x: np.ndarray[tuple[()], np.dtype[T_co]]) -> T_co:
    return x[()]  # type: ignore


def _false(shape: S_in) -> np.ndarray[S_in, np.dtype[np.bool]]:
    return np.zeros(shape, np.dtype(np.bool))  # type: ignore


def _fraction_to_scalar(x: Fraction) -> np.ndarray[tuple[()], np.dtype[_Fraction]]:
    return np.array(x)


def _full(shape: S_in, x: bool) -> np.ndarray[S_in, np.dtype[np.bool]]:
    return np.full(shape, x)  # type: ignore


def _greater(
    x: np.ndarray[S_co, np.dtype[T_co]],
    y: T_co | np.ndarray[S_co, np.dtype[T_co]],
    *,
    out: None | np.ndarray[S_co, np.dtype[np.bool]] = None,
    where: Literal[True] | np.ndarray[S_co, np.dtype[np.bool]] = True,
) -> np.ndarray[S_co, np.dtype[np.bool]]:
    return np.greater(x, y, out=out, where=where)  # type: ignore


def _greater_fraction(
    x: np.ndarray[S_co, np.dtype[_Fraction]], y: np.ndarray[S_co, np.dtype[_Fraction]]
) -> np.ndarray[S_co, np.dtype[np.bool]]:
    return x > y  # type: ignore


def _greater_equal(
    x: np.ndarray[S_co, np.dtype[T_co]],
    y: T_co | np.ndarray[S_co, np.dtype[T_co]],
) -> np.ndarray[S_co, np.dtype[np.bool]]:
    return x >= y  # type: ignore


def _greater_equal_fraction(
    x: np.ndarray[S_co, np.dtype[_Fraction]],
    y: Fraction | np.ndarray[S_co, np.dtype[_Fraction]],
) -> np.ndarray[S_co, np.dtype[np.bool]]:
    return x >= y  # type: ignore


def _isfinite(
    x: np.ndarray[S_co, np.dtype[T_co]],
) -> np.ndarray[S_co, np.dtype[np.bool]]:
    return np.isfinite(x)  # type: ignore


def _isinf(
    x: np.ndarray[S_co, np.dtype[T_co]],
) -> np.ndarray[S_co, np.dtype[np.bool]]:
    return np.isinf(x)  # type: ignore


def _isnan(
    x: np.ndarray[S_co, np.dtype[T_co]],
    *,
    out: None | np.ndarray[S_co, np.dtype[np.bool]] = None,
    where: Literal[True] | np.ndarray[S_co, np.dtype[np.bool]] = True,
) -> np.ndarray[S_co, np.dtype[np.bool]]:
    return np.isnan(x, out=out, where=where)  # type: ignore


def _less(
    x: np.ndarray[S_co, np.dtype[T_co]],
    y: T_co | np.ndarray[S_co, np.dtype[T_co]],
    *,
    out: None | np.ndarray[S_co, np.dtype[np.bool]] = None,
    where: Literal[True] | np.ndarray[S_co, np.dtype[np.bool]] = True,
) -> np.ndarray[S_co, np.dtype[np.bool]]:
    return np.less(x, y, out=out, where=where)  # type: ignore


def _less_fraction(
    x: np.ndarray[S_co, np.dtype[_Fraction]], y: np.ndarray[S_co, np.dtype[_Fraction]]
) -> np.ndarray[S_co, np.dtype[np.bool]]:
    return x < y  # type: ignore


def _less_equal(
    x: np.ndarray[S_co, np.dtype[T_co]], y: T_co | np.ndarray[S_co, np.dtype[T_co]]
) -> np.ndarray[S_co, np.dtype[np.bool]]:
    return x <= y  # type: ignore


def _less_equal_fraction(
    x: np.ndarray[S_co, np.dtype[_Fraction]],
    y: Fraction | np.ndarray[S_co, np.dtype[_Fraction]],
) -> np.ndarray[S_co, np.dtype[np.bool]]:
    return x <= y  # type: ignore


def _logical_and(
    x: np.ndarray[S_co, np.dtype[np.bool]],
    y: np.ndarray[S_co, np.dtype[np.bool]],
    *,
    out: None | np.ndarray[S_co, np.dtype[np.bool]] = None,
    where: Literal[True] | np.ndarray[S_co, np.dtype[np.bool]] = True,
) -> np.ndarray[S_co, np.dtype[np.bool]]:
    return np.logical_and(x, y, out=out, where=where)  # type: ignore


def _logical_or(
    x: np.ndarray[S_co, np.dtype[np.bool]], y: np.ndarray[S_co, np.dtype[np.bool]]
) -> np.ndarray[S_co, np.dtype[np.bool]]:
    return x | y  # type: ignore


def _multiply_fraction(
    x: np.ndarray[S_co, np.dtype[_Fraction]],
    y: Fraction | np.ndarray[S_co, np.dtype[_Fraction]],
) -> np.ndarray[S_co, np.dtype[_Fraction]]:
    return x * y  # type: ignore


def _nextafter(
    x: np.ndarray[S_co, np.dtype[_F_co]],
    y: _F_co | np.ndarray[S_co, np.dtype[_F_co]],
    *,
    out: None | np.ndarray[S_co, np.dtype[_F_co]] = None,
    where: Literal[True] | np.ndarray[S_co, np.dtype[np.bool]] = True,
) -> np.ndarray[S_co, np.dtype[_F_co]]:
    return np.nextafter(x, y, out=out, where=where)  # type: ignore


def _subtract(
    x: np.ndarray[S_co, np.dtype[T_co]], y: np.ndarray[S_co, np.dtype[T_co]]
) -> np.ndarray[S_co, np.dtype[T_co]]:
    return x - y  # type: ignore


def _subtract_fraction(
    x: np.ndarray[S_co, np.dtype[_Fraction]],
    y: Fraction | np.ndarray[S_co, np.dtype[_Fraction]],
) -> np.ndarray[S_co, np.dtype[_Fraction]]:
    return x - y  # type: ignore


def _rsubtract_fraction(
    x: Fraction | np.ndarray[S_co, np.dtype[_Fraction]],
    y: np.ndarray[S_co, np.dtype[_Fraction]],
) -> np.ndarray[S_co, np.dtype[T_co]]:
    return x - y  # type: ignore


def _sum_fraction(
    x: np.ndarray[S_co, np.dtype[_Fraction]],
    *,
    where: Literal[True] | np.ndarray[S_co, np.dtype[np.bool]] = True,
) -> Fraction:
    if x.size > 0:
        return np.sum(x, initial=Fraction(0), where=where)  # type: ignore
    return Fraction(0)


def _to_finite_or_zero(
    x: np.ndarray[S_co, np.dtype[_F_co]],
) -> np.ndarray[S_co, np.dtype[_F_co]]:
    return np.nan_to_num(x, nan=0, posinf=0, neginf=0)  # type: ignore


def _true(shape: S_in) -> np.ndarray[S_in, np.dtype[np.bool]]:
    return np.ones(shape, np.dtype(np.bool))  # type: ignore
