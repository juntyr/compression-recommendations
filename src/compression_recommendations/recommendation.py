from collections.abc import Collection, Mapping
from dataclasses import dataclass
from typing import Self, override

from .config import Config
from .filters.abc import Filter
from .requirements.abc import Requirement
from .typing import JSON


@dataclass(kw_only=True)
class Recommendation(Config):
    filters: Collection[Filter]
    requirements: Collection[Requirement]

    def matches(
        self, *, markers: Mapping[str, None | bool | int | float | str]
    ) -> bool:
        all_match = True

        for filter in self.filters:
            all_match &= filter.matches(markers=markers)

        return all_match

    @override
    @classmethod
    def from_config(  # type: ignore
        cls,
        *,
        filters: Collection[Mapping[str, JSON]],
        requirements: Collection[Mapping[str, JSON]],
    ) -> Self:
        return cls(
            filters=tuple(
                Filter.from_config(
                    **filter  # type: ignore
                )
                for filter in filters
            ),
            requirements=tuple(
                Requirement.from_config(
                    **requirement  # type: ignore
                )
                for requirement in requirements
            ),
        )

    @override
    def get_config(self) -> JSON:
        return dict(
            filters=tuple(filter.get_config() for filter in self.filters),
            requirements=tuple(
                requirement.get_config() for requirement in self.requirements
            ),
        )
