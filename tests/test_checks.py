import numpy as np
from compression_recommendation_checks import check_safety_requirement
from compression_safeguards.api import Safeguards
from compression_safeguards_recommendations import safeguards_for_requirement

from compression_recommendations.requirements.combinators import AnyRequirement
from compression_recommendations.requirements.error_bounds.mean import (
    MeanRangeRelativeErrorBoundRequirement,
    MeanRelativeErrorBoundRequirement,
)
from compression_recommendations.requirements.limits import DataLimitsRequirement
from compression_recommendations.requirements.lossless import LosslessRequirement


def test_fuzzer_found_mean_relative_error_1():
    original = np.array(
        [
            [1179010630],
            [1179010630],
            [1179010630],
            [1179010630],
            [1179010630],
            [1179010630],
            [0],
        ],
        dtype=np.uint32,
    )

    decompressed = np.array(
        [
            [0],
            [1179010630],
            [1179010630],
            [1179010630],
            [1179010630],
            [1179010630],
            [1179010630],
        ],
        dtype=np.uint32,
    )

    requirement = MeanRelativeErrorBoundRequirement(value=10)

    safeguards = Safeguards(safeguards=safeguards_for_requirement(requirement))

    correction = safeguards.compute_correction(
        data=original, approximation=decompressed
    )
    corrected = safeguards.apply_correction(
        approximation=decompressed, correction=correction
    )

    assert check_safety_requirement(
        original=original, reconstructed=corrected, requirement=requirement
    )


def test_fuzzer_found_mean_relative_error_2():
    original = np.array([[-1, -1, -1], [-1, -1, -1], [0, 0, 0]], dtype=np.int16)

    decompressed = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]], dtype=np.int16)

    requirement = MeanRelativeErrorBoundRequirement(value=1.7976657046605298e308)

    safeguards = Safeguards(safeguards=safeguards_for_requirement(requirement))

    correction = safeguards.compute_correction(
        data=original, approximation=decompressed
    )
    corrected = safeguards.apply_correction(
        approximation=decompressed, correction=correction
    )

    assert check_safety_requirement(
        original=original, reconstructed=corrected, requirement=requirement
    )


def test_fuzzer_found_any_data_limits_1():
    original = np.array([[0]], dtype=np.int32)

    decompressed = np.array([[370546176]], dtype=np.int32)

    requirement = AnyRequirement(
        requirements=[
            MeanRelativeErrorBoundRequirement(value=0.0),
            DataLimitsRequirement(minimum=0, maximum=22),
            DataLimitsRequirement(minimum=-1, maximum=0),
        ]
    )

    safeguards = Safeguards(safeguards=safeguards_for_requirement(requirement))

    correction = safeguards.compute_correction(
        data=original, approximation=decompressed
    )
    corrected = safeguards.apply_correction(
        approximation=decompressed, correction=correction
    )

    assert check_safety_requirement(
        original=original, reconstructed=corrected, requirement=requirement
    )


def test_fuzzer_found_any_data_limits_2():
    original = np.array([[22, 22], [58, 22]], dtype=np.uint8)

    decompressed = np.array([[207, 22], [22, 22]], dtype=np.uint8)

    requirement = AnyRequirement(
        requirements=[
            MeanRelativeErrorBoundRequirement(value=0.0),
            DataLimitsRequirement(minimum=0, maximum=22),
            LosslessRequirement(),
        ]
    )

    safeguards = Safeguards(safeguards=safeguards_for_requirement(requirement))

    correction = safeguards.compute_correction(
        data=original, approximation=decompressed
    )
    corrected = safeguards.apply_correction(
        approximation=decompressed, correction=correction
    )

    assert check_safety_requirement(
        original=original, reconstructed=corrected, requirement=requirement
    )


def test_fuzzer_found_mean_range_relative_error_1():
    original = np.array([[0.0007434], [0.001731]], dtype=np.float16)

    decompressed = np.array([[5.212e03], [np.nan]], dtype=np.float16)

    requirement = MeanRangeRelativeErrorBoundRequirement(value=44)

    safeguards = Safeguards(safeguards=safeguards_for_requirement(requirement))

    correction = safeguards.compute_correction(
        data=original,
        approximation=decompressed,
        late_bound={
            "$x_min": np.float16(0.0007434),
            "$x_max": np.float16(0.001731),
        },
    )
    corrected = safeguards.apply_correction(
        approximation=decompressed, correction=correction
    )

    assert check_safety_requirement(
        original=original, reconstructed=corrected, requirement=requirement
    )
