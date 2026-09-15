import atheris

with atheris.instrument_imports():
    import sys
    import types
    import typing
    import warnings
    from collections.abc import Collection
    from inspect import signature

    import numpy as np
    from compression_requirement_checks import check_safety_requirement
    from compression_safeguards import Safeguards
    from compression_safeguards.safeguards.pointwise.sign import SignPreservingSafeguard
    from compression_safeguards.utils._compat import _ensure_array
    from compression_safeguards.utils.bindings import Bindings
    from compression_safeguards.utils.error import (
        ErrorContextMixin,
        LateBoundParameterContextLayer,
        ParameterContextLayer,
        SafeguardTypeContextLayer,
    )
    from compression_safeguards.utils.typing import S, T
    from compression_safeguards_recommendations import safeguards_for_requirement

    from compression_recommendations.requirements.abc import Requirement
    from compression_recommendations.requirements.kind import RequirementKind


warnings.filterwarnings("error")


np.set_printoptions(floatmode="unique")


# the fuzzer *somehow* messes up np.nanmin and np.nanmax, so patch them
def nanmin(x: np.ndarray[S]) -> T:
    x = _ensure_array(x)
    if np.all(np.isnan(x)):
        warnings.warn("All-NaN slice encountered", RuntimeWarning)
        return x.dtype.type(np.nan)
    if np.any(np.isnan(x)):
        x = _ensure_array(x, copy=True)
        x[np.isnan(x)] = np.inf
    return np.amin(x)


np.nanmin = nanmin


def nanmax(x: np.ndarray[S, np.dtype[T]]) -> T:
    x = _ensure_array(x)
    if np.all(np.isnan(x)):
        warnings.warn("All-NaN slice encountered", RuntimeWarning)
        return x.dtype.type(np.nan)
    if np.any(np.isnan(x)):
        x = _ensure_array(x, copy=True)
        x[np.isnan(x)] = -np.inf
    return np.amax(x)


np.nanmax = nanmax


def generate_parameter(data: atheris.FuzzedDataProvider, ty: type, depth: int):
    if ty is types.NoneType:
        return None
    if ty is float:
        return data.ConsumeFloat()
    if ty is int:
        return data.ConsumeInt(1)

    if ty is Requirement:
        return generate_requirement(data, depth + 1)

    if typing.get_origin(ty) is Collection:
        if len(typing.get_args(ty)) == 1:
            return [
                generate_parameter(data, typing.get_args(ty)[0], depth)
                for _ in range(data.ConsumeIntInRange(0, max(0, 3 - depth)))
            ]

    if typing.get_origin(ty) in (typing.Union, types.UnionType):
        tys = typing.get_args(ty)

        ty = tys[data.ConsumeIntInRange(0, len(tys) - 1)]

        return generate_parameter(data, ty, depth)

    assert False, f"unknown parameter type {ty!r}"


def generate_requirement(data: atheris.FuzzedDataProvider, depth: int):
    cls = list(RequirementKind)[data.ConsumeIntInRange(0, len(RequirementKind) - 1)].cls

    return cls(
        **{
            p: generate_parameter(data, v.annotation, depth)
            for p, v in signature(cls).parameters.items()
        }
    )


def check_one_input(data) -> None:
    data = atheris.FuzzedDataProvider(data)

    try:
        requirement = generate_requirement(data, 0)
    except ValueError as err:
        if str(err) in [
            "minimum must not be NaN",
            "maximum must not be NaN",
            "minimum must be finite",
            "maximum must be finite",
            "maximum must be greater than minimum",
            "maximum must be greater than or equal to minimum",
            "error bound most be finite",
            "error bound must be non-negative",
        ]:
            return
        raise

    supported_dtypes = {
        np.dtype(np.uint8),
        np.dtype(np.int8),
        np.dtype(np.uint16),
        np.dtype(np.int16),
        np.dtype(np.uint32),
        np.dtype(np.int32),
        np.dtype(np.float16),
        np.dtype(np.float32),
        np.dtype(np.float64),
    }

    dtype: np.dtype[np.number] = np.dtype(
        sorted([d.name for d in supported_dtypes])[
            data.ConsumeIntInRange(0, len(supported_dtypes) - 1)
        ]
    )
    sizea: int = data.ConsumeIntInRange(0, 20)
    sizeb: int = data.ConsumeIntInRange(0, 20 // max(1, sizea))
    size = sizea * sizeb

    # input data and the decoded data
    raw = data.ConsumeBytes(size * dtype.itemsize)
    decoded = data.ConsumeBytes(size * dtype.itemsize)

    if len(raw) != size * dtype.itemsize:
        return

    if len(decoded) != size * dtype.itemsize:
        return

    raw = np.frombuffer(raw, dtype=dtype)
    decoded = np.frombuffer(decoded, dtype=dtype)

    if sizeb != 0:
        raw = raw.reshape((sizea, sizeb))
        decoded = decoded.reshape((sizea, sizeb))

    try:
        safeguards = Safeguards(safeguards=safeguards_for_requirement(requirement))
    except ValueError:
        return

    late_bound_reqs = safeguards.late_bound
    late_bound = Bindings()

    info = np.finfo(dtype) if np.issubdtype(dtype, np.floating) else np.iinfo(dtype)

    if "$x_min" in late_bound_reqs:
        late_bound = late_bound.update(
            **{
                "$x_min": np.nanmin(raw)
                if raw.size > 0 and not np.all(np.isnan(raw))
                else raw.dtype.type(0)
            }
        )
    if "$x_max" in late_bound_reqs:
        late_bound = late_bound.update(
            **{
                "$x_max": np.nanmax(raw)
                if raw.size > 0 and not np.all(np.isnan(raw))
                else raw.dtype.type(0)
            }
        )
    if "$x_finite_min" in late_bound_reqs:
        late_bound = late_bound.update(
            **{
                "$x_finite_min": np.amin(raw, where=np.isfinite(raw), initial=info.max)
                if raw.size > 0 and np.any(np.isfinite(raw))
                else raw.dtype.type(0)
            }
        )
    if "$x_finite_max" in late_bound_reqs:
        late_bound = late_bound.update(
            **{
                "$x_finite_max": np.amax(raw, where=np.isfinite(raw), initial=info.min)
                if raw.size > 0 and np.any(np.isfinite(raw))
                else raw.dtype.type(0)
            }
        )

    try:
        correction = safeguards.compute_correction(
            data=raw, approximation=decoded, late_bound=late_bound
        )

        corrected = safeguards.apply_correction(
            approximation=decoded, correction=correction
        )
    except Exception as err:
        if isinstance(err, ErrorContextMixin):
            match err.context.layers:
                case (*_, ParameterContextLayer(_)) | (
                    *_,
                    ParameterContextLayer(_),
                    LateBoundParameterContextLayer(_),
                ) if isinstance(err, TypeError | ValueError) and (
                    "cannot losslessly cast" in str(err)
                ):
                    return
                case (
                    *_,
                    ParameterContextLayer("eb"),
                    LateBoundParameterContextLayer(_),
                ) if (
                    isinstance(err, ValueError)
                    and ("cannot cast non-finite" in str(err))
                    and ("to saturating finite" in str(err))
                ):
                    return
                case (
                    *_,
                    ParameterContextLayer("eb"),
                    LateBoundParameterContextLayer(_),
                ) if isinstance(err, ValueError) and ("must be" in str(err)):
                    return
                case (
                    *_,
                    SafeguardTypeContextLayer(safeguard),
                    ParameterContextLayer("offset"),
                    LateBoundParameterContextLayer(_),
                ) if (
                    isinstance(err, ValueError)
                    and ("must not contain any NaN values" in str(err))
                    and safeguard is SignPreservingSafeguard
                ):
                    return
                case _:
                    pass
        print(  # noqa: T201
            f"\n===\n\nrequirement = {requirement!r}\n\nsafeguards = {safeguards!r}\n\noriginal = {raw!r}\n\ndecompressed = {decoded!r}\n\n===\n"
        )
        raise

    try:
        if not check_safety_requirement(
            original=raw, reconstructed=corrected, requirement=requirement
        ):
            raise RuntimeError("safeguards do not preserve safety requirement")
    except Exception:
        print(  # noqa: T201
            f"\n===\n\nrequirement = {requirement!r}\n\nsafeguards = {safeguards!r}\n\noriginal = {raw!r}\n\ndecompressed = {decoded!r}\n\ncorrected = {corrected!r}\n\n===\n"
        )
        raise


atheris.Setup(sys.argv, check_one_input)
atheris.Fuzz()
