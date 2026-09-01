"""
Abstract base class for JSON-configurable types.
"""

from abc import ABC, abstractmethod
from collections.abc import Mapping
from enum import StrEnum
from types import MappingProxyType, NoneType
from typing import TYPE_CHECKING, Literal, Self, TypeAlias, assert_never, final

if TYPE_CHECKING:
    from .filters.abc import Filter
    from .requirements.abc import Requirement

import strictyaml
from typing_extensions import Reader, Writer  # MSPV 3.14

from .typing import JSON

__all__ = ["Config", "Format", "LiteralFormat"]


LiteralFormat: TypeAlias = Literal["plain", "terminal"]


class Format(StrEnum):
    plain = "plain"
    terminal = "terminal"

    @classmethod
    def from_literal(cls, format: LiteralFormat | Self) -> Self:
        return cls[format]

    def as_literal(self) -> LiteralFormat:
        return self.value


class Config(ABC):
    __slots__: tuple[str, ...] = ()

    @classmethod
    @abstractmethod
    def from_config(cls, **kwargs: JSON) -> Self: ...

    @abstractmethod
    def get_config(self) -> Mapping[str, JSON]: ...

    @abstractmethod
    def humanise(self, *, format: LiteralFormat | Format = Format.plain) -> str: ...

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


def _humanise_kinded_type(
    this: "Filter | Requirement", *, format: LiteralFormat | Format = Format.plain
) -> str:
    kind_kebap = type(this).kind.value
    kind_camel = _to_camel_case(kind_kebap)

    return _humanise_labelled_type(this, label=kind_camel, format=format)


def _humanise_labelled_type(
    this: object, *, label: str, format: LiteralFormat | Format = Format.plain
) -> str:
    ty = type(this)
    format = Format.from_literal(format)

    match format:
        case Format.plain:
            return label
        case Format.terminal:
            uri = f"https://juntyr.github.io/compression-recommendations/_ref/{ty.__module__.replace('.', '/')}/#{ty.__module__}.{ty.__name__}"
            return _hyperlink(uri, label)
        case _:
            assert_never(format)


# based on https://stackoverflow.com/a/19053800
def _to_camel_case(kebap_case: str) -> str:
    return "".join(x.capitalize() for x in kebap_case.lower().split("-"))


# based on https://stackoverflow.com/a/71309268
def _hyperlink(uri: str, label: None | str = None):
    if label is None:
        label = uri

    parameters = ""

    # OSC 8 ; params ; URI ST <name> OSC 8 ;; ST
    escape_mask = "\033]8;{};{}\033\\{}\033]8;;\033\\"

    return escape_mask.format(parameters, uri, label)
