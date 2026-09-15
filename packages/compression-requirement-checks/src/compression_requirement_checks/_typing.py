from typing import TypeVar, final

import numpy as np

__all__ = ["_F_co", "_Fraction"]

_F_co = TypeVar("_F_co", bound=np.float16 | np.float32 | np.float64, covariant=True)


@final
class _Fraction(np.object_):  # type: ignore
    pass
