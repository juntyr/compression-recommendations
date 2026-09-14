from collections.abc import Collection

import numpy as np
from compression_recommendations.requirements.abc import Requirement

from .._compat import _assign_and, _assign_or, _false, _true
from ..typing import S_co, T_co

__all__ = ["_check_any", "_check_all"]


def _check_any(
    *,
    original: np.ndarray[S_co, np.dtype[T_co]],
    reconstructed: np.ndarray[S_co, np.dtype[T_co]],
    requirements: Collection[Requirement],
) -> np.ndarray[S_co, np.dtype[np.bool]]:
    from . import _check_safety_requirement_pointwise  # noqa: PLC0415

    ok: np.ndarray[S_co, np.dtype[np.bool]] = _false(original.shape)
    for requirement in requirements:
        _assign_or(
            ok,
            _check_safety_requirement_pointwise(
                original=original, reconstructed=reconstructed, requirement=requirement
            ),
        )
    return ok


def _check_all(
    *,
    original: np.ndarray[S_co, np.dtype[T_co]],
    reconstructed: np.ndarray[S_co, np.dtype[T_co]],
    requirements: Collection[Requirement],
) -> np.ndarray[S_co, np.dtype[np.bool]]:
    from . import _check_safety_requirement_pointwise  # noqa: PLC0415

    ok: np.ndarray[S_co, np.dtype[np.bool]] = _true(original.shape)
    for requirement in requirements:
        _assign_and(
            ok,
            _check_safety_requirement_pointwise(
                original=original, reconstructed=reconstructed, requirement=requirement
            ),
        )
    return ok
