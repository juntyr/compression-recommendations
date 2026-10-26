import pytest

from compression_recommendations.filters.abc import Filter
from compression_recommendations.filters.cf import (
    CfShortNameFilter,
    CfStandardNameFilter,
)
from compression_recommendations.filters.combinators import (
    AllFilters,
    AnyFilter,
    NotFilter,
)
from compression_recommendations.filters.grib import GribShortNameFilter
from compression_recommendations.filters.level import (
    LevelKind,
    LevelKindFilter,
    LevelValueFilter,
)
from compression_recommendations.filters.tag import TagFilter
from compression_recommendations.requirements.abc import Requirement
from compression_recommendations.requirements.combinators import (
    AllRequirements,
    AnyRequirement,
)
from compression_recommendations.requirements.error_bounds.max import (
    MaxPointwiseAbsoluteErrorBoundRequirement,
    MaxPointwiseQuadraticErrorBoundRequirement,
    MaxPointwiseRangeRelativeErrorBoundRequirement,
    MaxPointwiseRelativeErrorBoundRequirement,
)
from compression_recommendations.requirements.error_bounds.mean import (
    MeanAbsoluteErrorBoundRequirement,
    MeanRangeRelativeErrorBoundRequirement,
    MeanRelativeErrorBoundRequirement,
)
from compression_recommendations.requirements.isovalue import IsovalueRequirement
from compression_recommendations.requirements.limits import DataLimitsRequirement
from compression_recommendations.requirements.lossless import LosslessRequirement
from compression_recommendations.requirements.missing import MissingValueRequirement


def assert_filter_roundtrip(filter: Filter):
    filter_str = filter.dumps()
    filter2 = Filter.loads(filter_str)
    assert filter.humanise() == filter2.humanise()


def assert_requirement_roundtrip(requirement: Requirement):
    requirement_str = requirement.dumps()
    requirement2 = Requirement.loads(requirement_str)
    assert requirement.humanise() == requirement2.humanise()


@pytest.mark.parametrize("cls", [AnyFilter, AllFilters])
def test_combinator_filter(cls):
    assert_filter_roundtrip(cls(filters=[]))
    assert_filter_roundtrip(cls(filters=[CfShortNameFilter(value="cc")]))
    assert_filter_roundtrip(
        cls(filters=[CfShortNameFilter(value="u"), CfShortNameFilter(value="v")])
    )


def test_not_combinator_filter():
    assert_filter_roundtrip(NotFilter(filter=CfShortNameFilter(value="cc")))


@pytest.mark.parametrize(
    "cls",
    [CfShortNameFilter, CfStandardNameFilter, GribShortNameFilter],
)
def test_variable_name_filter(cls):
    assert_filter_roundtrip(cls(value="cc"))


def test_level_kind_filter():
    assert_filter_roundtrip(LevelKindFilter(value=LevelKind.single))
    assert_filter_roundtrip(LevelKindFilter(value=LevelKind.pressure))


def test_level_value_filter():
    assert_filter_roundtrip(LevelValueFilter())
    assert_filter_roundtrip(LevelValueFilter(minimum=-4))
    assert_filter_roundtrip(LevelValueFilter(maximum=+2))
    assert_filter_roundtrip(LevelValueFilter(minimum=-4, maximum=+2))


def test_test_filter():
    assert_filter_roundtrip(TagFilter(value="tagged"))


@pytest.mark.parametrize("cls", [AnyRequirement, AllRequirements])
def test_combinator_requirement(cls):
    assert_requirement_roundtrip(cls(requirements=[IsovalueRequirement(value=0)]))
    assert_requirement_roundtrip(
        cls(requirements=[IsovalueRequirement(value=0), IsovalueRequirement(value=1)])
    )


def test_empty_all_combinator_requirement():
    assert_requirement_roundtrip(AllRequirements(requirements=[]))


@pytest.mark.parametrize(
    "cls",
    [
        MaxPointwiseAbsoluteErrorBoundRequirement,
        MaxPointwiseRelativeErrorBoundRequirement,
        MaxPointwiseRangeRelativeErrorBoundRequirement,
        MeanAbsoluteErrorBoundRequirement,
        MeanRelativeErrorBoundRequirement,
        MeanRangeRelativeErrorBoundRequirement,
    ],
)
def test_error_bound_requirement(cls):
    assert_requirement_roundtrip(cls(value=4.2))


def test_quadrartic_error_bound_requirement():
    assert_requirement_roundtrip(
        MaxPointwiseQuadraticErrorBoundRequirement(value=4.2, minimum=-10, maximum=10)
    )


def test_data_limits_requirement():
    assert_requirement_roundtrip(DataLimitsRequirement())
    assert_requirement_roundtrip(DataLimitsRequirement(minimum=-10))
    assert_requirement_roundtrip(DataLimitsRequirement(maximum=10))
    assert_requirement_roundtrip(DataLimitsRequirement(minimum=-10, maximum=10))


def test_isovalue_requirement():
    assert_requirement_roundtrip(IsovalueRequirement(value=4.2))


def test_missing_value_requirement():
    assert_requirement_roundtrip(MissingValueRequirement(value=99999))
    assert_requirement_roundtrip(MissingValueRequirement(value=-0.0))
    assert_requirement_roundtrip(MissingValueRequirement(value=float("nan")))


def test_lossless_requirement():
    assert_requirement_roundtrip(LosslessRequirement())
