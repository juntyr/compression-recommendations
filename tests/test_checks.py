import numpy as np
from compression_recommendation_checks import check_safety_requirement
from compression_safeguards.api import Safeguards
from compression_safeguards_recommendations import safeguards_for_requirement

from compression_recommendations.requirements.error_bounds.mean import (
    MeanRelativeErrorBoundRequirement,
)


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
