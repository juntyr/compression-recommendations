"""
Commonly used type variables and type aliases.
"""

__all__ = ["JSON"]

from collections.abc import Collection, Mapping
from typing import TypeAlias

JSON: TypeAlias = (
    None | int | float | str | bool | Collection["JSON"] | Mapping[str, "JSON"]
)
""" Types that are valid read-only JSON and can be encoded with [`json.dumps`][json.dumps]. """
