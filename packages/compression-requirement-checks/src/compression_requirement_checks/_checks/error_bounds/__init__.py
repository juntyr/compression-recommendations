import math
from fractions import Fraction

__all__ = ["_check_error_bound"]


def _check_error_bound(x: int | float) -> Fraction:
    if x < 0:
        raise ValueError("error bound must be non-negative")

    if not math.isfinite(x):
        raise ValueError("error bound most be finite")

    return Fraction(x)
