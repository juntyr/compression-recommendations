"""
Logical combinations of multiple requirements.
"""

from collections.abc import Collection, Mapping
from dataclasses import dataclass
from typing import ClassVar, Literal, Self

from typing_extensions import override  # MSPV 3.12

from ..typing import JSON
from .abc import Requirement
from .kind import RequirementKind

__all__ = ["AnyRequirement", "AllRequirements"]


@dataclass(kw_only=True)
class AnyRequirement(Requirement):
    kind: ClassVar[RequirementKind] = RequirementKind.any
    requirements: Collection[Requirement]

    @override
    @classmethod
    def from_config(  # type: ignore
        cls,
        *,
        requirements: Collection[Mapping[str, JSON]],
        kind: Literal["any"] = RequirementKind.any.value,
    ) -> Self:
        return cls(
            requirements=tuple(
                Requirement.from_config(
                    **requirement  # type: ignore
                )
                for requirement in requirements
            )
        )

    @override
    def get_config(self) -> JSON:
        return dict(
            kind=type(self).kind.get_config(),
            requirements=[
                requirement.get_config() for requirement in self.requirements
            ],
        )


@dataclass(kw_only=True)
class AllRequirements(Requirement):
    kind: ClassVar[RequirementKind] = RequirementKind.all
    requirements: Collection[Requirement]

    @override
    @classmethod
    def from_config(  # type: ignore
        cls,
        *,
        requirements: Collection[Mapping[str, JSON]],
        kind: Literal["all"] = RequirementKind.all.value,
    ) -> Self:
        return cls(
            requirements=tuple(
                Requirement.from_config(
                    **requirement  # type: ignore
                )
                for requirement in requirements
            )
        )

    @override
    def get_config(self) -> JSON:
        return dict(
            kind=type(self).kind.get_config(),
            requirements=[
                requirement.get_config() for requirement in self.requirements
            ],
        )
