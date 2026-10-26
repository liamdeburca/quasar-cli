from collections import defaultdict

import click
from quasar_errors.analysis import Analyser
from quasar_errors.analysis.measure_result import FrozenMeasureResult
from quasar_utils.pipeline import SubDir

from quasar_cli.cli.context import _Ctx
from quasar_cli.utils import _map

from .validation import (
    validate_bg_flux,
    validate_h,
    validate_name,
    validate_p,
    validate_q,
    validate_unit,
    validate_x_bounds,
)


def _measure_helper(
    *,
    ctx: _Ctx,
    name: str,
    method_name: str,
    unit: str | None,
    start: int,
    stop: int,
    verbose: bool,
    force: bool,
    progress: bool,
    fail_fast: bool,
    **kwargs,
) -> None:
    """Helper that runs a measurement method across all analysers in ctx.

    All parameters are keyword-only to avoid accidental positional calls from
    callers. Extra measurement-specific parameters are forwarded via kwargs.
    """
    with ctx:
        assert "analysers" in ctx

        name = validate_name(ctx, name, force)
        if unit:
            unit = validate_unit(unit)

        method = getattr(Analyser, method_name)

        results: dict[str, dict[str, FrozenMeasureResult]] = defaultdict(dict)

        msgs: list[str] = [f"Failed to measure ({name})"]

        def func(i: int, subdir: SubDir):
            key = subdir.in_file.stem
            try:
                analyser = ctx.analysers[key]
            except KeyError:
                msgs.append(f"{key}: {i=}, could not find Analyser")
                return 


            try:
                res: FrozenMeasureResult = method(analyser, **kwargs)
                if unit:
                    res = res.to(unit)

                results[key][name] = res
            except Exception as exc:
                msgs.append(f"{key}: {i=}, {exc=}")
                if fail_fast:
                    click.echo("\n".join(msgs))
                    raise
                return

        it = list(ctx.output_dir)
        _map(
            func, it,
            start=start,
            stop=stop,
            progress=progress,
            desc_func=lambda subdir: f"{name} - {subdir.out_dir.stem}",
            leave=False,
        )

        for key, res_dict in results.items():
            if not ctx.results._get_path(key).exists():
                ctx.results[key] = {}
            ctx.results[key].update(res_dict)

        if verbose and len(msgs) > 1:
            click.echo("\n".join(msgs))


def _mode(
    *,
    ctx: _Ctx,
    name: str,
    bg: tuple[str, ...],
    unit: str,
    start: int,
    stop: int,
    from_model: bool,
    verbose: bool,
    force: bool,
    progress: bool,
    fail_fast: bool,
) -> None:
    _measure_helper(
        ctx=ctx,
        name=name,
        method_name="measureMode",
        unit=unit,
        start=start,
        stop=stop,
        verbose=verbose,
        force=force,
        progress=progress,
        fail_fast=fail_fast,
        from_model=from_model,
        bg_flux=validate_bg_flux(bg),
    )


def _mode_off(
    *,
    ctx: _Ctx,
    name: str,
    bg: tuple[str, ...],
    unit: str,
    start: int,
    stop: int,
    from_model: bool,
    verbose: bool,
    force: bool,
    progress: bool,
    fail_fast: bool,
) -> None:
    _measure_helper(
        ctx=ctx,
        name=name,
        method_name="measureModeOffset",
        unit=unit,
        start=start,
        stop=stop,
        verbose=verbose,
        force=force,
        progress=progress,
        fail_fast=fail_fast,
        from_model=from_model,
        bg_flux=validate_bg_flux(bg),
    )


def _max(
    *,
    ctx: _Ctx,
    name: str,
    bg: tuple[str, ...],
    unit: str,
    start: int,
    stop: int,
    from_model: bool,
    verbose: bool,
    force: bool,
    progress: bool,
    fail_fast: bool,
) -> None:
    _measure_helper(
        ctx=ctx,
        name=name,
        method_name="measureMax",
        unit=unit,
        start=start,
        stop=stop,
        verbose=verbose,
        force=force,
        progress=progress,
        fail_fast=fail_fast,
        from_model=from_model,
        bg_flux=validate_bg_flux(bg),
    )


def _fwhm(
    *,
    ctx: _Ctx,
    h: float,
    name: str,
    bg: tuple[str, ...],
    unit: str,
    start: int,
    stop: int,
    from_model: bool,
    verbose: bool,
    force: bool,
    progress: bool,
    fail_fast: bool,
) -> None:
    _measure_helper(
        ctx=ctx,
        name=name,
        method_name="measureFWHM",
        unit=unit,
        start=start,
        stop=stop,
        verbose=verbose,
        force=force,
        progress=progress,
        fail_fast=fail_fast,
        h=validate_h(h),
        from_model=from_model,
        bg_flux=validate_bg_flux(bg),
    )


def _fwhm_vel(
    *,
    ctx: _Ctx,
    h: float,
    name: str,
    bg: tuple[str, ...],
    unit: str,
    start: int,
    stop: int,
    from_model: bool,
    verbose: bool,
    force: bool,
    progress: bool,
    fail_fast: bool,
) -> None:
    _measure_helper(
        ctx=ctx,
        name=name,
        method_name="measureFWHMVelocity",
        unit=unit,
        start=start,
        stop=stop,
        verbose=verbose,
        force=force,
        progress=progress,
        fail_fast=fail_fast,
        h=validate_h(h),
        from_model=from_model,
        bg_flux=validate_bg_flux(bg),
    )


def _w_k1(
    *,
    ctx: _Ctx,
    name: str,
    bg: tuple[str, ...],
    unit: str,
    start: int,
    stop: int,
    from_model: bool,
    verbose: bool,
    force: bool,
    progress: bool,
    fail_fast: bool,
) -> None:
    _measure_helper(
        ctx=ctx,
        name=name,
        method_name="measureWhittleK1",
        unit=unit,
        start=start,
        stop=stop,
        verbose=verbose,
        force=force,
        progress=progress,
        fail_fast=fail_fast,
        from_model=from_model,
        bg_flux=validate_bg_flux(bg),
    )


def _w_k2(
    *,
    ctx: _Ctx,
    name: str,
    bg: tuple[str, ...],
    unit: str,
    start: int,
    stop: int,
    from_model: bool,
    verbose: bool,
    force: bool,
    progress: bool,
    fail_fast: bool,
) -> None:
    _measure_helper(
        ctx=ctx,
        name=name,
        method_name="measureWhittleK2",
        unit=unit,
        start=start,
        stop=stop,
        verbose=verbose,
        force=force,
        progress=progress,
        fail_fast=fail_fast,
        from_model=from_model,
        bg_flux=validate_bg_flux(bg),
    )


def _mad(
    *,
    ctx: _Ctx,
    name: str,
    bg: tuple[str, ...],
    unit: str,
    start: int,
    stop: int,
    from_model: bool,
    verbose: bool,
    force: bool,
    progress: bool,
    fail_fast: bool,
) -> None:
    _measure_helper(
        ctx=ctx,
        name=name,
        method_name="measureMAD",
        unit=unit,
        start=start,
        stop=stop,
        verbose=verbose,
        force=force,
        progress=progress,
        fail_fast=fail_fast,
        from_model=from_model,
        bg_flux=validate_bg_flux(bg),
    )


def _mad_vel(
    *,
    ctx: _Ctx,
    name: str,
    bg: tuple[str, ...],
    unit: str,
    start: int,
    stop: int,
    from_model: bool,
    verbose: bool,
    force: bool,
    progress: bool,
    fail_fast: bool,
) -> None:
    _measure_helper(
        ctx=ctx,
        name=name,
        method_name="measureMADVelocity",
        unit=unit,
        start=start,
        stop=stop,
        verbose=verbose,
        force=force,
        progress=progress,
        fail_fast=fail_fast,
        from_model=from_model,
        bg_flux=validate_bg_flux(bg),
    )


def _aad(
    *,
    ctx: _Ctx,
    name: str,
    bg: tuple[str, ...],
    unit: str,
    start: int,
    stop: int,
    from_model: bool,
    verbose: bool,
    force: bool,
    progress: bool,
    fail_fast: bool,
) -> None:
    _measure_helper(
        ctx=ctx,
        name=name,
        method_name="measureAAD",
        unit=unit,
        start=start,
        stop=stop,
        verbose=verbose,
        force=force,
        progress=progress,
        fail_fast=fail_fast,
        from_model=from_model,
        bg_flux=validate_bg_flux(bg),
    )


def _aad_vel(
    *,
    ctx: _Ctx,
    name: str,
    bg: tuple[str, ...],
    unit: str,
    start: int,
    stop: int,
    from_model: bool,
    verbose: bool,
    force: bool,
    progress: bool,
    fail_fast: bool,
) -> None:
    _measure_helper(
        ctx=ctx,
        name=name,
        method_name="measureAADVelocity",
        unit=unit,
        start=start,
        stop=stop,
        verbose=verbose,
        force=force,
        progress=progress,
        fail_fast=fail_fast,
        from_model=from_model,
        bg_flux=validate_bg_flux(bg),
    )


def _lum(
    *,
    ctx: _Ctx,
    lb: float,
    ub: float,
    name: str,
    bg: tuple[str, ...],
    unit: str,
    start: int,
    stop: int,
    from_model: bool,
    verbose: bool,
    force: bool,
    progress: bool,
    fail_fast: bool,
) -> None:
    _measure_helper(
        ctx=ctx,
        name=name,
        method_name="measureIntegratedFlux",
        unit=unit,
        start=start,
        stop=stop,
        verbose=verbose,
        force=force,
        progress=progress,
        fail_fast=fail_fast,
        from_model=from_model,
        bg_flux=validate_bg_flux(bg),
        x_bounds=validate_x_bounds(lb, ub),
    )


def _flux(
    *,
    ctx: _Ctx,
    lb: float,
    ub: float,
    name: str,
    bg: tuple[str, ...],
    unit: str,
    start: int,
    stop: int,
    from_model: bool,
    verbose: bool,
    force: bool,
    progress: bool,
    fail_fast: bool,
) -> None:
    _measure_helper(
        ctx=ctx,
        name=name,
        method_name="measureAverageFluxDensity",
        unit=unit,
        start=start,
        stop=stop,
        verbose=verbose,
        force=force,
        progress=progress,
        fail_fast=fail_fast,
        from_model=from_model,
        bg_flux=validate_bg_flux(bg),
        x_bounds=validate_x_bounds(lb, ub),
    )


def _ew(
    *,
    ctx: _Ctx,
    name: str,
    unit: str,
    start: int,
    stop: int,
    from_model: bool,
    verbose: bool,
    force: bool,
    progress: bool,
    fail_fast: bool,
) -> None:
    _measure_helper(
        ctx=ctx,
        name=name,
        method_name="measureEW",
        unit=unit,
        start=start,
        stop=stop,
        verbose=verbose,
        force=force,
        progress=progress,
        fail_fast=fail_fast,
        from_model=from_model,
    )


def _strength(
    *,
    ctx: _Ctx,
    name: str,
    bg: tuple[str, ...],
    unit: str,
    start: int,
    stop: int,
    from_model: bool,
    verbose: bool,
    force: bool,
    progress: bool,
    fail_fast: bool,
) -> None:
    _measure_helper(
        ctx=ctx,
        name=name,
        method_name="measureZerothMoment",
        unit=unit,
        start=start,
        stop=stop,
        verbose=verbose,
        force=force,
        progress=progress,
        fail_fast=fail_fast,
        from_model=from_model,
        bg_flux=validate_bg_flux(bg),
    )


def _cen(
    *,
    ctx: _Ctx,
    name: str,
    bg: tuple[str, ...],
    unit: str,
    start: int,
    stop: int,
    from_model: bool,
    verbose: bool,
    force: bool,
    progress: bool,
    fail_fast: bool,
) -> None:
    _measure_helper(
        ctx=ctx,
        name=name,
        method_name="measureFirstMoment",
        unit=unit,
        start=start,
        stop=stop,
        verbose=verbose,
        force=force,
        progress=progress,
        fail_fast=fail_fast,
        from_model=from_model,
        bg_flux=validate_bg_flux(bg),
    )


def _cen_off(
    *,
    ctx: _Ctx,
    name: str,
    bg: tuple[str, ...],
    unit: str,
    start: int,
    stop: int,
    from_model: bool,
    verbose: bool,
    force: bool,
    progress: bool,
    fail_fast: bool,
) -> None:
    _measure_helper(
        ctx=ctx,
        name=name,
        method_name="measureMeanOffset",
        unit=unit,
        start=start,
        stop=stop,
        verbose=verbose,
        force=force,
        progress=progress,
        fail_fast=fail_fast,
        from_model=from_model,
        bg_flux=validate_bg_flux(bg),
    )


def _cm2(
    *,
    ctx: _Ctx,
    name: str,
    bg: tuple[str, ...],
    unit: str,
    start: int,
    stop: int,
    from_model: bool,
    verbose: bool,
    force: bool,
    progress: bool,
    fail_fast: bool,
) -> None:
    _measure_helper(
        ctx=ctx,
        name=name,
        method_name="measureSecondCentralMoment",
        unit=unit,
        start=start,
        stop=stop,
        verbose=verbose,
        force=force,
        progress=progress,
        fail_fast=fail_fast,
        from_model=from_model,
        bg_flux=validate_bg_flux(bg),
    )


def _disp(
    *,
    ctx: _Ctx,
    name: str,
    bg: tuple[str, ...],
    unit: str,
    start: int,
    stop: int,
    from_model: bool,
    verbose: bool,
    force: bool,
    progress: bool,
    fail_fast: bool,
) -> None:
    _measure_helper(
        ctx=ctx,
        name=name,
        method_name="measureDispersion",
        unit=unit,
        start=start,
        stop=stop,
        verbose=verbose,
        force=force,
        progress=progress,
        fail_fast=fail_fast,
        from_model=from_model,
        bg_flux=validate_bg_flux(bg),
    )


def _disp_vel(
    *,
    ctx: _Ctx,
    name: str,
    bg: tuple[str, ...],
    unit: str,
    start: int,
    stop: int,
    from_model: bool,
    verbose: bool,
    force: bool,
    progress: bool,
    fail_fast: bool,
) -> None:
    _measure_helper(
        ctx=ctx,
        name=name,
        method_name="measureVelocityDispersion",
        unit=unit,
        start=start,
        stop=stop,
        verbose=verbose,
        force=force,
        progress=progress,
        fail_fast=fail_fast,
        from_model=from_model,
        bg_flux=validate_bg_flux(bg),
    )


def _skew(
    *,
    ctx: _Ctx,
    name: str,
    bg: tuple[str, ...],
    unit: str,
    start: int,
    stop: int,
    from_model: bool,
    verbose: bool,
    force: bool,
    progress: bool,
    fail_fast: bool,
) -> None:
    _measure_helper(
        ctx=ctx,
        name=name,
        method_name="measureSkewness",
        unit=unit,
        start=start,
        stop=stop,
        verbose=verbose,
        force=force,
        progress=progress,
        fail_fast=fail_fast,
        from_model=from_model,
        bg_flux=validate_bg_flux(bg),
    )


def _kurt(
    *,
    ctx: _Ctx,
    name: str,
    bg: tuple[str, ...],
    unit: str,
    start: int,
    stop: int,
    from_model: bool,
    excess: bool,
    verbose: bool,
    force: bool,
    progress: bool,
    fail_fast: bool,
) -> None:
    _measure_helper(
        ctx=ctx,
        name=name,
        method_name="measureKurtosis",
        unit=unit,
        start=start,
        stop=stop,
        verbose=verbose,
        force=force,
        progress=progress,
        fail_fast=fail_fast,
        from_model=from_model,
        bg_flux=validate_bg_flux(bg),
        excess=excess,
    )


def _q(
    *,
    ctx: _Ctx,
    q: float,
    name: str,
    bg: tuple[str, ...],
    unit: str,
    start: int,
    stop: int,
    from_model: bool,
    verbose: bool,
    force: bool,
    progress: bool,
    fail_fast: bool,
) -> None:
    _measure_helper(
        ctx=ctx,
        name=name,
        method_name="measureQuantile",
        unit=unit,
        start=start,
        stop=stop,
        verbose=verbose,
        force=force,
        progress=progress,
        fail_fast=fail_fast,
        q=validate_q(q),
        from_model=from_model,
        bg_flux=validate_bg_flux(bg),
    )


def _med(
    *,
    ctx: _Ctx,
    name: str,
    bg: tuple[str, ...],
    unit: str,
    start: int,
    stop: int,
    from_model: bool,
    verbose: bool,
    force: bool,
    progress: bool,
    fail_fast: bool,
) -> None:
    _measure_helper(
        ctx=ctx,
        name=name,
        method_name="measureMedian",
        unit=unit,
        start=start,
        stop=stop,
        verbose=verbose,
        force=force,
        progress=progress,
        fail_fast=fail_fast,
        from_model=from_model,
        bg_flux=validate_bg_flux(bg),
    )


def _med_off(
    *,
    ctx: _Ctx,
    name: str,
    bg: tuple[str, ...],
    unit: str,
    start: int,
    stop: int,
    from_model: bool,
    verbose: bool,
    force: bool,
    progress: bool,
    fail_fast: bool,
) -> None:
    _measure_helper(
        ctx=ctx,
        name=name,
        method_name="measureMedianOffset",
        unit=unit,
        start=start,
        stop=stop,
        verbose=verbose,
        force=force,
        progress=progress,
        fail_fast=fail_fast,
        from_model=from_model,
        bg_flux=validate_bg_flux(bg),
    )


def _ipw(
    *,
    ctx: _Ctx,
    p: float,
    name: str,
    bg: tuple[str, ...],
    unit: str,
    start: int,
    stop: int,
    from_model: bool,
    verbose: bool,
    force: bool,
    progress: bool,
    fail_fast: bool,
) -> None:
    _measure_helper(
        ctx=ctx,
        name=name,
        method_name="measureIPWidth",
        unit=unit,
        start=start,
        stop=stop,
        verbose=verbose,
        force=force,
        progress=progress,
        fail_fast=fail_fast,
        p=validate_p(p),
        from_model=from_model,
        bg_flux=validate_bg_flux(bg),
    )


def _ipv(
    *,
    ctx: _Ctx,
    p: float,
    name: str,
    bg: tuple[str, ...],
    unit: str,
    start: int,
    stop: int,
    from_model: bool,
    verbose: bool,
    force: bool,
    progress: bool,
    fail_fast: bool,
) -> None:
    _measure_helper(
        ctx=ctx,
        name=name,
        method_name="measureIPVelocity",
        unit=unit,
        start=start,
        stop=stop,
        verbose=verbose,
        force=force,
        progress=progress,
        fail_fast=fail_fast,
        p=validate_p(p),
        from_model=from_model,
        bg_flux=validate_bg_flux(bg),
    )


def _w_a(
    *,
    ctx: _Ctx,
    p: float,
    name: str,
    bg: tuple[str, ...],
    unit: str,
    start: int,
    stop: int,
    from_model: bool,
    verbose: bool,
    force: bool,
    progress: bool,
    fail_fast: bool,
) -> None:
    _measure_helper(
        ctx=ctx,
        name=name,
        method_name="measureWhittleA",
        unit=unit,
        start=start,
        stop=stop,
        verbose=verbose,
        force=force,
        progress=progress,
        fail_fast=fail_fast,
        p=validate_p(p),
        from_model=from_model,
        bg_flux=validate_bg_flux(bg),
    )


def _w_b(
    *,
    ctx: _Ctx,
    p: float,
    name: str,
    bg: tuple[str, ...],
    unit: str,
    start: int,
    stop: int,
    from_model: bool,
    verbose: bool,
    force: bool,
    progress: bool,
    fail_fast: bool,
) -> None:
    _measure_helper(
        ctx=ctx,
        name=name,
        method_name="measureWhittleB",
        unit=unit,
        start=start,
        stop=stop,
        verbose=verbose,
        force=force,
        progress=progress,
        fail_fast=fail_fast,
        p=validate_p(p),
        from_model=from_model,
        bg_flux=validate_bg_flux(bg),
    )


def _w_shi(
    *,
    ctx: _Ctx,
    p: float,
    name: str,
    bg: tuple[str, ...],
    unit: str,
    start: int,
    stop: int,
    from_model: bool,
    verbose: bool,
    force: bool,
    progress: bool,
    fail_fast: bool,
) -> None:
    _measure_helper(
        ctx=ctx,
        name=name,
        method_name="measureWhittleShift",
        unit=unit,
        start=start,
        stop=stop,
        verbose=verbose,
        force=force,
        progress=progress,
        fail_fast=fail_fast,
        p=validate_p(p),
        from_model=from_model,
        bg_flux=validate_bg_flux(bg),
    )


def _w_asy(
    *,
    ctx: _Ctx,
    p: float,
    name: str,
    bg: tuple[str, ...],
    unit: str,
    start: int,
    stop: int,
    from_model: bool,
    verbose: bool,
    force: bool,
    progress: bool,
    fail_fast: bool,
) -> None:
    _measure_helper(
        ctx=ctx,
        name=name,
        method_name="measureWhittleAsymmetry",
        unit=unit,
        start=start,
        stop=stop,
        verbose=verbose,
        force=force,
        progress=progress,
        fail_fast=fail_fast,
        p=validate_p(p),
        from_model=from_model,
        bg_flux=validate_bg_flux(bg),
    )
