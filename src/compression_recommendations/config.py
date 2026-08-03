"""
Abstract base class for JSON-configurable types.
"""

from abc import ABC, abstractmethod
from collections.abc import Mapping
from types import MappingProxyType, NoneType
from typing import Self, final

import strictyaml
from typing_extensions import Reader, Writer  # MSPV 3.14

from .typing import JSON

__all__ = ["Config"]


class Config(ABC):
    __slots__: tuple[str, ...] = ()

    @classmethod
    @abstractmethod
    def from_config(cls, **kwargs: JSON) -> Self:
        pass

    @abstractmethod
    def get_config(self) -> Mapping[str, JSON]:
        pass

    @final
    @classmethod
    def loads(cls, yaml: str) -> Self:
        return cls.from_config(
            **_parse_yaml(  # type: ignore
                strictyaml.load(yaml)
            )
        )

    @final
    @classmethod
    def load(cls, reader: Reader[str]) -> Self:
        return cls.loads(reader.read())

    @final
    def dumps(self) -> str:
        return strictyaml.as_document(self.get_config()).as_yaml()

    @final
    def dump(self, writer: Writer[str]) -> None:
        writer.write(self.dumps())


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


# FIXME: use a schema for strictyaml instead
def _parse_number(x: int | float | str) -> int | float:
    if isinstance(x, int | float):
        return x
    try:
        return int(x)
    except ValueError:
        return float(x)
