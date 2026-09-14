import numpy as np
from compression_recommendation_checks import check_safety_requirement
from compression_safeguards.api import Safeguards
from compression_safeguards_recommendations import safeguards_for_requirement

from compression_recommendations.requirements.combinators import (
    AllRequirements,
    AnyRequirement,
)
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
from compression_recommendations.requirements.isovalue import IsovalueRequirement
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
            "$x_finite_min": np.float16(0.0007434),
            "$x_finite_max": np.float16(0.001731),
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
            "$x_finite_min": np.float32(0.0),
            "$x_finite_max": np.float32(0.0),
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
            "$x_finite_min": np.float32(0.0),
            "$x_finite_max": np.float32(0.0),
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
            "$x_finite_min": np.float32(0.0),
            "$x_finite_max": np.float32(0.0),
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


def test_fuzzer_found_data_limits_outside_both_1():
    original = np.array([[1.308e01], [-2.928e-04], [-2.775e-04]], dtype=np.float16)

    decompressed = np.array([[-2.775e-04], [-2.775e-04], [-8.380e02]], dtype=np.float16)

    requirement = AnyRequirement(
        requirements=[
            DataLimitsRequirement(minimum=0, maximum=0.0),
            AllRequirements(
                requirements=[
                    MaxPointwiseRangeRelativeErrorBoundRequirement(value=38),
                    MeanRelativeErrorBoundRequirement(value=38),
                ]
            ),
            MeanRelativeErrorBoundRequirement(value=38),
        ]
    )

    safeguards = Safeguards(safeguards=safeguards_for_requirement(requirement))

    correction = safeguards.compute_correction(
        data=original,
        approximation=decompressed,
        late_bound={
            "$x_finite_min": np.float16(-2.928e-04),
            "$x_finite_max": np.float16(1.308e01),
        },
    )
    corrected = safeguards.apply_correction(
        approximation=decompressed, correction=correction
    )

    assert check_safety_requirement(
        original=original, reconstructed=corrected, requirement=requirement
    )


def test_fuzzer_found_range_relative_zero_error_bound_1():
    original = np.array(
        [
            [0.000e00],
            [-3.200e02],
            [2.092e-05],
            [-1.920e01],
            [np.nan],
            [3.058e04],
            [1.010e-01],
            [2.135e-02],
            [2.928e04],
            [7.093e-06],
            [9.656e-02],
            [9.601e-02],
            [np.nan],
            [-1.384e-04],
            [-4.362e01],
            [np.nan],
            [-3.942e04],
        ],
        dtype=np.float16,
    )

    decompressed = np.array(
        [
            [np.nan],
            [9.656e-02],
            [9.656e-02],
            [9.656e-02],
            [2.023e-02],
            [9.656e-02],
            [9.656e-02],
            [-1.276e-04],
            [3.275e04],
            [-2.278e-04],
            [2.023e-02],
            [9.375e-02],
            [np.nan],
            [1.093e-01],
            [-1.276e-04],
            [-1.268e-04],
            [-2.354e-01],
        ],
        dtype=np.float16,
    )

    requirement = MeanRangeRelativeErrorBoundRequirement(value=0)

    safeguards = Safeguards(safeguards=safeguards_for_requirement(requirement))

    correction = safeguards.compute_correction(
        data=original,
        approximation=decompressed,
        late_bound={
            "$x_finite_min": np.float16(-3.942e04),
            "$x_finite_max": np.float16(3.058e04),
        },
    )
    corrected = safeguards.apply_correction(
        approximation=decompressed, correction=correction
    )

    assert check_safety_requirement(
        original=original, reconstructed=corrected, requirement=requirement
    )


def test_fuzzer_found_range_relative_zero_error_bound_2():
    original = np.array(
        [[0.000e00], [9.600e01], [1.633e-05], [-np.inf]], dtype=np.float16
    )

    decompressed = np.array(
        [[-3.315e02], [0.000e00], [9.900e-02], [9.656e-02]], dtype=np.float16
    )

    requirement = AnyRequirement(
        requirements=[
            MeanRangeRelativeErrorBoundRequirement(value=0),
            MeanRangeRelativeErrorBoundRequirement(value=0),
            MeanRangeRelativeErrorBoundRequirement(value=0),
        ]
    )

    safeguards = Safeguards(safeguards=safeguards_for_requirement(requirement))

    correction = safeguards.compute_correction(
        data=original,
        approximation=decompressed,
        late_bound={
            "$x_finite_min": np.float16(0.0),
            "$x_finite_max": np.float16(9.600e01),
        },
    )
    corrected = safeguards.apply_correction(
        approximation=decompressed, correction=correction
    )

    assert check_safety_requirement(
        original=original, reconstructed=corrected, requirement=requirement
    )


def test_fuzzer_found_data_limits_outside_both_2():
    original = np.array([[-1.876e-04], [-1.716e01], [np.nan]], dtype=np.float16)

    decompressed = np.array([[7.739e-04], [-5.256e03], [np.nan]], dtype=np.float16)

    requirement = AnyRequirement(
        requirements=[
            DataLimitsRequirement(minimum=0, maximum=0.0),
            AllRequirements(
                requirements=[
                    MaxPointwiseRangeRelativeErrorBoundRequirement(value=38),
                    MeanRelativeErrorBoundRequirement(value=38),
                ]
            ),
            MeanAbsoluteErrorBoundRequirement(value=38),
        ]
    )

    safeguards = Safeguards(safeguards=safeguards_for_requirement(requirement))

    correction = safeguards.compute_correction(
        data=original,
        approximation=decompressed,
        late_bound={
            "$x_finite_min": np.float16(-1.716e01),
            "$x_finite_max": np.float16(-1.876e-04),
        },
    )
    corrected = safeguards.apply_correction(
        approximation=decompressed, correction=correction
    )

    assert check_safety_requirement(
        original=original, reconstructed=corrected, requirement=requirement
    )


def test_fuzzer_found_global_safeguard_any_ok_if_any_ok_1():
    original = np.array(
        [
            [-721420288],
            [-707406379],
            [6346069],
            [-721420288],
            [-863371051],
            [826105198],
            [1641403861],
            [1596577132],
            [16223],
            [-863371264],
            [826105198],
            [1641403861],
            [-707406484],
            [-718482125],
            [14013909],
            [0],
            [-721420288],
            [-707406379],
            [6346069],
        ],
        dtype=np.int32,
    )

    decompressed = np.array(
        [
            [-721420288],
            [-43],
            [1596550399],
            [16223],
            [-863371264],
            [826105198],
            [-100608555],
            [869651967],
            [-707449643],
            [54741],
            [0],
            [-707461120],
            [1440077269],
            [24789],
            [-707461120],
            [-1],
            [1600072044],
            [63],
            [1858898432],
        ],
        dtype=np.int32,
    )

    requirement = AnyRequirement(
        requirements=[
            MeanAbsoluteErrorBoundRequirement(value=96),
            MeanRelativeErrorBoundRequirement(value=1.5809822920694217e293),
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


def test_fuzzer_found_quadratic_error_rounding_error_1():
    original = np.array([[3.450e01]], dtype=np.float16)

    decompressed = np.array([[1.276e-04]], dtype=np.float16)

    requirement = MaxPointwiseQuadraticErrorBoundRequirement(
        value=1, minimum=0, maximum=95
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


def test_fuzzer_found_quadratic_error_rounding_error_2():
    original = np.array(
        [
            [249, 255],
            [255, 44],
            [255, 255],
            [255, 255],
            [255, 255],
            [255, 255],
            [255, 255],
            [255, 255],
        ],
        dtype=np.uint8,
    )

    decompressed = np.array(
        [[255, 255], [255, 255], [251, 255], [8, 0], [46, 8], [0, 0], [0, 1], [15, 15]],
        dtype=np.uint8,
    )

    requirement = MaxPointwiseQuadraticErrorBoundRequirement(
        value=1, minimum=-23, maximum=95
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


def test_fuzzer_found_quadratic_error_rounding_error_3():
    original = np.array(
        [[74, 1, 0, 16, -113, 86], [86, 86, 86, 86, -1, -1]], dtype=np.int8
    )

    decompressed = np.array(
        [[-1, -1, -1, -1, -1, -1], [86, 86, 86, 86, 86, 36]], dtype=np.int8
    )

    requirement = AnyRequirement(
        requirements=[
            MaxPointwiseQuadraticErrorBoundRequirement(value=21, minimum=0, maximum=41),
            MaxPointwiseQuadraticErrorBoundRequirement(value=0, minimum=0, maximum=3),
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


def test_fuzzer_found_quadratic_error_rounding_error_4():
    original = np.array(
        [
            [233, 1],
            # [249, 255],
            # [255, 255],
            # [255, 255],
            # [255, 255],
            # [255, 255],
            # [255, 255],
            [93, 64],
        ],
        dtype=np.uint8,
    )

    decompressed = np.array(
        [
            [255, 255],
            # [255, 255],
            # [255, 255],
            # [255, 251],
            # [255, 8],
            # [0, 46],
            # [8, 0],
            [0, 0],
        ],
        dtype=np.uint8,
    )

    requirement = MaxPointwiseQuadraticErrorBoundRequirement(
        value=49, minimum=-35, maximum=95
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


def test_fuzzer_found_quadratic_error_rounding_error_5():
    original = np.array(
        [[0.000e00, 1.628e-04], [3.000e00, 9.600e01], [2.475e-02, 1.014e02]],
        dtype=np.float16,
    )

    decompressed = np.array(
        [[6.384e-02, 1.014e02], [9.838e01, 1.547e-03], [1.507e-03, 1.014e02]],
        dtype=np.float16,
    )

    requirement = AnyRequirement(
        requirements=[
            MaxPointwiseQuadraticErrorBoundRequirement(value=47, minimum=0, maximum=1),
            AllRequirements(
                requirements=[
                    MaxPointwiseQuadraticErrorBoundRequirement(
                        value=21, minimum=0, maximum=74
                    ),
                    AnyRequirement(
                        requirements=[
                            MaxPointwiseQuadraticErrorBoundRequirement(
                                value=17, minimum=-35, maximum=0
                            )
                        ]
                    ),
                ]
            ),
            AllRequirements(
                requirements=[
                    MaxPointwiseQuadraticErrorBoundRequirement(
                        value=0, minimum=0, maximum=86
                    ),
                    MaxPointwiseQuadraticErrorBoundRequirement(
                        value=49, minimum=-35, maximum=126
                    ),
                ]
            ),
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


def test_fuzzer_found_global_safeguard_any_ok_if_any_ok_2():
    original = np.array(
        [
            [-1.157e01, 1.788e-05, 4.484e03],
            [-1.157e01, -1.157e01, -1.157e01],
            [-1.157e01, -1.157e01, -1.157e01],
        ],
        dtype=np.float16,
    )

    decompressed = np.array(
        [
            [-1.157e01, -1.808e-01, 2.402e-02],
            [2.402e-02, 1.520e-05, 1.876e-04],
            [1.698e-04, -1.157e01, -1.157e01],
        ],
        dtype=np.float16,
    )

    requirement = AnyRequirement(
        requirements=[
            MeanAbsoluteErrorBoundRequirement(value=44),
            IsovalueRequirement(value=-0.0),
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


def test_fuzzer_found_range_relative_finite_range_1():
    original = np.array(
        [[0.0], [-np.inf], [np.nan]],
        dtype=np.float16,
    )

    decompressed = np.array(
        [[0.1093], [0.1931], [-0.1562]],
        dtype=np.float16,
    )

    requirement = AnyRequirement(
        requirements=[
            LosslessRequirement(),
            MeanRangeRelativeErrorBoundRequirement(value=46),
            MeanRangeRelativeErrorBoundRequirement(value=1),
        ]
    )

    safeguards = Safeguards(safeguards=safeguards_for_requirement(requirement))

    correction = safeguards.compute_correction(
        data=original,
        approximation=decompressed,
        late_bound={
            "$x_finite_min": np.float16(0.0),
            "$x_finite_max": np.float16(0.0),
        },
    )
    corrected = safeguards.apply_correction(
        approximation=decompressed, correction=correction
    )

    assert check_safety_requirement(
        original=original, reconstructed=corrected, requirement=requirement
    )


def test_fuzzer_found_range_relative_finite_range_2():
    original = np.array(
        [
            [-np.inf, 1.01e-06],
            [np.nan, 1.52e-05],
            [0.00e00, 0.00e00],
            [0.00e00, 0.00e00],
        ],
        dtype=np.float16,
    )

    decompressed = np.array(
        [
            [0.000e00, 0.000e00],
            [0.000e00, 0.000e00],
            [-4.272e-04, -2.560e03],
            [-2.048e03, -8.376e03],
        ],
        dtype=np.float16,
    )

    requirement = AnyRequirement(
        requirements=[
            MeanRangeRelativeErrorBoundRequirement(value=78),
            MeanRangeRelativeErrorBoundRequirement(value=44),
            AnyRequirement(
                requirements=[
                    MeanRangeRelativeErrorBoundRequirement(value=0),
                    MeanRangeRelativeErrorBoundRequirement(value=0),
                ]
            ),
        ]
    )

    safeguards = Safeguards(safeguards=safeguards_for_requirement(requirement))

    correction = safeguards.compute_correction(
        data=original,
        approximation=decompressed,
        late_bound={
            "$x_finite_min": np.float16(0.0),
            "$x_finite_max": np.float16(1.52e-05),
        },
    )
    corrected = safeguards.apply_correction(
        approximation=decompressed, correction=correction
    )

    assert check_safety_requirement(
        original=original, reconstructed=corrected, requirement=requirement
    )


def test_fuzzer_found_range_relative_rounding_error_1():
    original = np.array([[-0.1175]], dtype=np.float16)

    decompressed = np.array([[-0.12006]], dtype=np.float16)

    requirement = requirement = AnyRequirement(
        requirements=[
            MaxPointwiseRangeRelativeErrorBoundRequirement(value=10),
            MaxPointwiseRangeRelativeErrorBoundRequirement(value=18),
            MeanRelativeErrorBoundRequirement(value=0),
        ]
    )

    safeguards = Safeguards(safeguards=safeguards_for_requirement(requirement))

    correction = safeguards.compute_correction(
        data=original,
        approximation=decompressed,
        late_bound={
            "$x_finite_min": np.float16(-0.1175),
            "$x_finite_max": np.float16(-0.1175),
        },
    )
    corrected = safeguards.apply_correction(
        approximation=decompressed, correction=correction
    )

    assert check_safety_requirement(
        original=original, reconstructed=corrected, requirement=requirement
    )
