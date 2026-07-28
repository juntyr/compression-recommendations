"""
Commonly used type variables.
"""

__all__ = ["JSON"]

from collections.abc import Collection, Mapping
from types import MappingProxyType, NoneType
from typing import TypeAlias

import strictyaml

JSON: TypeAlias = (
    None | int | float | str | bool | Collection["JSON"] | Mapping[str, "JSON"]
)


def _parse_yaml(yaml: strictyaml.YAML) -> JSON:
    if isinstance(yaml.value, NoneType | int | float | str | bool):
        return yaml.value

    if isinstance(yaml.value, list):
        return tuple(_parse_yaml(x) for x in yaml.value)

    if isinstance(yaml.value, dict):
        return MappingProxyType(
            {_parse_yaml(k): _parse_yaml(v) for k, v in yaml.value.items()}
        )

    raise ValueError("unexpected yaml", yaml)
