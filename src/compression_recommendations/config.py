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
""" Literal strings representing the humanised representation [`Format`][..Format]s. """


class Format(StrEnum):
    """
    Enumeration of humanised representation formats.
    """

    plain = "plain"
    """ Plain-text format. """

    terminal = "terminal"
    """ Format for printing to the terminal, which uses ANSII escape sequences. """

    @classmethod
    def from_literal(cls, format: LiteralFormat | Self) -> Self:
        """
        Convert a literal format string into its corresponding format enum variant.

        Parameters
        ----------
        format : LiteralFormat | Self
            The literal format string, or format enum variant.

        Returns
        -------
        format : Self
            The format enum variant.
        """

        return cls[format]

    @property
    def literal(self) -> LiteralFormat:
        """
        Get the literal format string for this format enum variant.
        """

        return self.value


class Config(ABC):
    """
    Abstract base class for [`JSON`][compression_recommendations.typing.JSON]-configurable classes.
    """

    __slots__: tuple[str, ...] = ()

    @classmethod
    @abstractmethod
    def from_config(cls, **kwargs: JSON) -> Self:
        """
        Construct a class instance from its [`JSON`][compression_recommendations.typing.JSON] configuration.

        Parameters
        ----------
        **kwargs : JSON
            The configuration.

        Returns
        -------
        instance : Self
            The instantiated class.
        """

    @abstractmethod
    def get_config(self) -> Mapping[str, JSON]:
        """
        Get the configuration of this instance.

        Returns
        -------
        config : Mapping[str, JSON]
            Configuration in JSON object format.
        """

    @abstractmethod
    def humanise(self, *, format: LiteralFormat | Format = Format.plain) -> str:
        """
        Humanise the representation of this instance.

        Parameters
        ----------
        format : Format | LiteralFormat
            The format of the humanised representation.

        Returns
        -------
        humanised : str
            The humanised representation of this instance.
        """

    @final
    @classmethod
    def loads(cls, yaml: str) -> Self:
        """
        Load an instance from its configuration, stored in YAML format in the `yaml` string.

        Parameters
        ----------
        yaml : str
            The serialised YAML configuration.

        Returns
        -------
        instance : Self
            The instantiated class.
        """

        return cls.from_config(
            **_parse_yaml(  # type: ignore
                strictyaml.load(yaml)
            )
        )

    @final
    @classmethod
    def load(cls, reader: Reader[str]) -> Self:
        """
        Load an instance from its configuration, read in YAML format from the `reader`, e.g. an [`open`][open]ed readable text file.

        Parameters
        ----------
        reader : Reader[str]
            The reader from which the YAML configuration is read.

        Returns
        -------
        instance : Self
            The serialised YAML configuration.
        """

        return cls.loads(reader.read())

    @final
    def dumps(self) -> str:
        """
        Serialise the configuration of this instance into a YAML string.

        Returns
        -------
        yaml : str
            The instantiated class.
        """

        return strictyaml.as_document(self.get_config()).as_yaml()

    @final
    def dump(self, writer: Writer[str]) -> None:
        """
        Serialise the configuration of this instance in YAML format to the provided `writer`, e.g. an [`open`][open]ed writable text file.

        Parameters
        ----------
        writer : Writer[str]
            The writer to which the YAML configuration is written.
        """

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
            return _terminal_hyperlink(uri, label)
        case _:
            assert_never(format)


# based on https://stackoverflow.com/a/19053800
def _to_camel_case(kebap_case: str) -> str:
    return "".join(x.capitalize() for x in kebap_case.lower().split("-"))


# based on https://stackoverflow.com/a/71309268
def _terminal_hyperlink(uri: str, label: None | str = None):
    if label is None:
        label = uri

    parameters = ""

    # OSC 8 ; params ; URI ST <name> OSC 8 ;; ST
    escape_mask = "\033]8;{};{}\033\\{}\033]8;;\033\\"

    return escape_mask.format(parameters, uri, label)
