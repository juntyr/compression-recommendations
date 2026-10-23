"""
Abstract base class for requirements.
"""

from abc import ABC
from typing import ClassVar, Self

import strictyaml
import strictyaml.compound
from typing_extensions import override  # MSPV 3.12

from ..config import Config
from ..typing import JSON
from .kind import RequirementKind

__all__ = ["Requirement"]


class Requirement(Config, ABC):
    """
    Abstract base class for requirements, which define the safety requirements that lossy compression must uphold.
    """

    __slots__: tuple[str, ...] = ()

    kind: ClassVar[RequirementKind]

    @override
    @classmethod
    def from_config(cls, *, kind: str, **kwargs: JSON) -> Self:  # type: ignore
        """
        Construct the specific requirement from its `kind` and [`JSON`][compression_recommendations.typing.JSON] configuration.

        Parameters
        ----------
        kind : str
            The requirement kind.
        **kwargs : JSON
            The requirement configuration.

        Returns
        -------
        requirement : Self
            The instantiated requirement.
        """

        return RequirementKind.from_config(kind=kind).cls.from_config(
            **kwargs  # type: ignore
        )

    @override
    @classmethod
    def _schema(cls) -> strictyaml.Validator:
        return _RequirementValidator()


class _RequirementValidator(strictyaml.compound.MapValidator):
    def validate(self, chunk):
        items = chunk.expect_mapping()

        for key, value in items:
            yaml_key = self.key_validator(key)
            if yaml_key == "kind":
                break
        else:
            chunk.while_parsing_found("a requirement", "required key 'kind' not found")

        yaml_value = RequirementKind._schema().validate(value)

        cls = RequirementKind.from_config(kind=yaml_value.value).cls

        return cls._schema().validate(chunk)

    def to_yaml(self, data):
        self._should_be_mapping(data)

        if "kind" not in data:
            raise ValueError("required key 'kind' not found for requirement")

        cls = RequirementKind.from_config(kind=data["kind"]).cls

        return cls._schema().to_yaml(data)

    @property
    def key_validator(self):
        return strictyaml.Str()
