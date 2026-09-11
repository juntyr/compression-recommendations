import numpy as np
from compression_recommendation_checks import check_safety_requirement
from compression_safeguards.api import Safeguards
from compression_safeguards_recommendations import safeguards_for_requirement

from compression_recommendations.requirements.combinators import AnyRequirement
from compression_recommendations.requirements.error_bounds.max import (
    MaxPointwiseQuadraticErrorBoundRequirement,
    MaxPointwiseRangeRelativeErrorBoundRequirement,
    MaxPointwiseRelativeErrorBoundRequirement,
)
from compression_recommendations.requirements.error_bounds.mean import (
    MeanAbsoluteErrorBoundRequirement,
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


def test_fuzzer_found_max_range_relative_error_nan_1():
    original = np.array([[np.nan]], dtype=np.float32)

    decompressed = np.array([[-3.3961514e38]], dtype=np.float32)

    requirement = AnyRequirement(
        requirements=[MaxPointwiseRangeRelativeErrorBoundRequirement(value=58)]
    )

    safeguards = Safeguards(safeguards=safeguards_for_requirement(requirement))

    correction = safeguards.compute_correction(
        data=original,
        approximation=decompressed,
        late_bound={
            "$x_min": np.float32(0.0),
            "$x_max": np.float32(0.0),
        },
    )
    corrected = safeguards.apply_correction(
        approximation=decompressed, correction=correction
    )

    assert check_safety_requirement(
        original=original, reconstructed=corrected, requirement=requirement
    )


def test_fuzzer_found_max_range_relative_error_nan_2():
    original = np.array([[np.nan]], dtype=np.float32)

    decompressed = np.array([[-0.0005149841]], dtype=np.float32)

    requirement = MaxPointwiseRangeRelativeErrorBoundRequirement(
        value=1.797637952589245e308
    )

    safeguards = Safeguards(safeguards=safeguards_for_requirement(requirement))

    correction = safeguards.compute_correction(
        data=original,
        approximation=decompressed,
        late_bound={
            "$x_min": np.float32(0.0),
            "$x_max": np.float32(0.0),
        },
    )
    corrected = safeguards.apply_correction(
        approximation=decompressed, correction=correction
    )

    assert check_safety_requirement(
        original=original, reconstructed=corrected, requirement=requirement
    )


def test_fuzzer_found_mean_range_relative_error_nan_1():
    original = np.array([[np.nan]], dtype=np.float32)

    decompressed = np.array([[-2.6584558e36]], dtype=np.float32)

    requirement = MeanRangeRelativeErrorBoundRequirement(value=1.797665811814156e308)

    safeguards = Safeguards(safeguards=safeguards_for_requirement(requirement))

    correction = safeguards.compute_correction(
        data=original,
        approximation=decompressed,
        late_bound={
            "$x_min": np.float32(0.0),
            "$x_max": np.float32(0.0),
        },
    )
    corrected = safeguards.apply_correction(
        approximation=decompressed, correction=correction
    )

    assert check_safety_requirement(
        original=original, reconstructed=corrected, requirement=requirement
    )


def test_fuzzer_found_any_mean_1():
    original = np.array([[0, 18], [141, 18], [85, 133]], dtype=np.uint8)

    decompressed = np.array([[85, 85], [85, 85], [85, 255]], dtype=np.uint8)

    requirement = AnyRequirement(
        requirements=[
            AnyRequirement(
                requirements=[
                    MeanRelativeErrorBoundRequirement(value=18),
                    MeanAbsoluteErrorBoundRequirement(value=3),
                ]
            )
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


def test_fuzzer_found_any_mean_2():
    original = np.array(
        [
            [0, 65305],
            [29423, 45037],
            [21847, 21845],
            [1621, 1542],
            [1542, 1542],
            [1542, 1542],
        ],
        dtype=np.uint16,
    )

    decompressed = np.array(
        [
            [1542, 1542],
            [1542, 1542],
            [1542, 1542],
            [1542, 1542],
            [1542, 1542],
            [1542, 1542],
        ],
        dtype=np.uint16,
    )

    requirement = AnyRequirement(
        requirements=[
            MeanRelativeErrorBoundRequirement(value=0),
            MeanAbsoluteErrorBoundRequirement(value=9),
            MeanRelativeErrorBoundRequirement(value=36),
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


def test_fuzzer_found_max_quadratic_error_1():
    original = np.array([[49, 66, -35, 1, 3], [50, -1, -1, -1, 85]], dtype=np.int8)

    decompressed = np.array([[85, 0, -43, 4, 49], [66, -35, 1, 3, 0]], dtype=np.int8)

    requirement = MaxPointwiseQuadraticErrorBoundRequirement(
        value=2.3407183170921814e305, minimum=-43, maximum=4
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


def test_fuzzer_found_max_quadratic_error_2():
    original = np.array([[49, 66, -35, 9, 3], [0, 18, -115, 18, 85]], dtype=np.int8)

    decompressed = np.array(
        [[0, -11, 4, 49, 66], [86, 18, -115, 18, 85]], dtype=np.int8
    )

    requirement = MaxPointwiseQuadraticErrorBoundRequirement(
        value=1.7204576235615554e308, minimum=-43, maximum=4
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


def test_fuzzer_found_max_quadratic_error_3():
    original = np.array([[-1, -1], [-2, -1]], dtype=np.int8)

    decompressed = np.array([[-1, -1], [65, 48]], dtype=np.int8)

    requirement = MaxPointwiseQuadraticErrorBoundRequirement(
        value=2.1340915476744706e306, minimum=-81, maximum=-1
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


def test_fuzzer_found_max_quadratic_error_4():
    original = np.array([[0, 0, 0, 0, 0], [0, 18, 85, 0, -11]], dtype=np.int8)

    decompressed = np.array([[4, 49, 86, 66, 18], [-115, 18, 85, 5, 86]], dtype=np.int8)

    requirement = MaxPointwiseQuadraticErrorBoundRequirement(
        value=1.7204576235615554e308, minimum=-115, maximum=0
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


def test_fuzzer_found_max_relative_1():
    original = np.array([[-8.647088e17]], dtype=np.float32)

    decompressed = np.array([[3.1675382e-38]], dtype=np.float32)

    requirement = MaxPointwiseRelativeErrorBoundRequirement(value=1)

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
