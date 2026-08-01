"""
Commonly used type variables.
"""

__all__ = ["JSON"]

from collections.abc import Collection, Mapping
from typing import TypeAlias

JSON: TypeAlias = (
    None | int | float | str | bool | Collection["JSON"] | Mapping[str, "JSON"]
)
