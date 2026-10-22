from quasar_utils.pipeline import SubDir

from quasar_cli.cli.context import _Ctx

from . import utils


def _plot_validate_context(ctx: _Ctx) -> None:
    """Validate that the context is properly set prior to plotting."""
    with ctx:
        _ = ctx.output_dir # Will crash if not set


def _spectrum_quick(
    *,
    ctx: _Ctx,
    # Options
    name: str,
    styles: tuple[str, ...],
    dpi: int,
    start: int,
    stop: int,
    # Flags
    progress: bool,
    force: bool,
    verbose: bool,
    fail_fast: bool,
):
    def plot_func(ctx: _Ctx, subdir: SubDir) -> None:
        utils._spectrum_quickplot(
            ctx=ctx,
            subdir=subdir,
            name=name,
            dpi=dpi,
            verbose=verbose & (not progress),
            force=force,
        )
    
    utils._plot_spectra_helper(
        ctx=ctx,
        plot_func=plot_func,
        styles=styles,
        start=start,
        stop=stop,
        progress=progress,
        verbose=verbose,
        fail_fast=fail_fast,
    )


def _spectrum_difference(
    *,
    ctx: _Ctx,
    # Options
    name: str,
    styles: tuple[str, ...],
    dpi: int,
    start: int,
    stop: int,
    # Flags
    residual: bool,
    progress: bool,
    force: bool,
    verbose: bool,
    fail_fast: bool,
):
    def plot_func(ctx: _Ctx, subdir: SubDir) -> None:
        utils._spectrum_differenceplot(
            ctx=ctx,
            subdir=subdir,
            name=name,
            dpi=dpi,
            residual=residual,
            verbose=verbose & (not progress),
            force=force,
        )

    utils._plot_spectra_helper(
        ctx=ctx,
        plot_func=plot_func,
        styles=styles,
        start=start,
        stop=stop,
        progress=progress,
        verbose=verbose,
        fail_fast=fail_fast,
    )

### WINDOWS

def _powerlaw_windows(
    *,
    ctx: _Ctx,
    # Options
    name: str,
    styles: tuple[str, ...],
    dpi: int,
    start: int,
    stop: int,
    # Flags
    residual: bool,
    progress: bool,
    force: bool,
    verbose: bool,
    fail_fast: bool,
):
    def plot_func(ctx: _Ctx, subdir: SubDir) -> None:
        utils._powerlaw_windows(
            ctx=ctx,
            subdir=subdir,
            name=name,
            dpi=dpi,
            residual=residual,
            verbose=verbose & (not progress),
            force=force,
        )

    utils._plot_spectra_helper(
        ctx=ctx,
        plot_func=plot_func,
        styles=styles,
        start=start,
        stop=stop,
        progress=progress,
        verbose=verbose,
        fail_fast=fail_fast,
    )

def _iron_windows(
    *,
    ctx: _Ctx,
    # Options
    name: str,
    styles: tuple[str, ...],
    dpi: int,
    start: int,
    stop: int,
    # Flags
    residual: bool,
    progress: bool,
    force: bool,
    verbose: bool,
    fail_fast: bool,
):
    def plot_func(ctx: _Ctx, subdir: SubDir) -> None:
        utils._iron_windows(
            ctx=ctx,
            subdir=subdir,
            name=name,
            dpi=dpi,
            residual=residual,
            verbose=verbose & (not progress),
            force=force,
        )

    utils._plot_spectra_helper(
        ctx=ctx,
        plot_func=plot_func,
        styles=styles,
        start=start,
        stop=stop,
        progress=progress,
        verbose=verbose,
        fail_fast=fail_fast,
    )

def _balmer_windows(
    *,
    ctx: _Ctx,
    # Options
    name: str,
    styles: tuple[str, ...],
    dpi: int,
    start: int,
    stop: int,
    # Flags
    residual: bool,
    progress: bool,
    force: bool,
    verbose: bool,
    fail_fast: bool,
):
    def plot_func(ctx: _Ctx, subdir: SubDir) -> None:
        utils._balmer_windows(
            ctx=ctx,
            subdir=subdir,
            name=name,
            dpi=dpi,
            residual=residual,
            verbose=verbose & (not progress),
            force=force,
        )

    utils._plot_spectra_helper(
        ctx=ctx,
        plot_func=plot_func,
        styles=styles,
        start=start,
        stop=stop,
        progress=progress,
        verbose=verbose,
        fail_fast=fail_fast,
    )

def _host_windows(
    *,
    ctx: _Ctx,
    # Options
    name: str,
    styles: tuple[str, ...],
    dpi: int,
    start: int,
    stop: int,
    # Flags
    residual: bool,
    progress: bool,
    force: bool,
    verbose: bool,
    fail_fast: bool,
):
    def plot_func(ctx: _Ctx, subdir: SubDir) -> None:
        utils._host_windows(
            ctx=ctx,
            subdir=subdir,
            name=name,
            dpi=dpi,
            residual=residual,
            verbose=verbose & (not progress),
            force=force,
        )

    utils._plot_spectra_helper(
        ctx=ctx,
        plot_func=plot_func,
        styles=styles,
        start=start,
        stop=stop,
        progress=progress,
        verbose=verbose,
        fail_fast=fail_fast,
    )

### TEMPLATES

def _iron_templates(
    *,
    ctx: _Ctx,
    # Options
    name: str,
    styles: tuple[str, ...],
    dpi: int,
    start: int,
    stop: int,
    # Flags
    residual: bool,
    progress: bool,
    force: bool,
    verbose: bool,
    fail_fast: bool,
):
    def plot_func(ctx: _Ctx, subdir: SubDir) -> None:
        utils._iron_templates(
            ctx=ctx,
            subdir=subdir,
            name=name,
            dpi=dpi,
            residual=residual,
            verbose=verbose & (not progress),
            force=force,
        )

    utils._plot_spectra_helper(
        ctx=ctx,
        plot_func=plot_func,
        styles=styles,
        start=start,
        stop=stop,
        progress=progress,
        verbose=verbose,
        fail_fast=fail_fast,
    )

def _balmer_templates(
    *,
    ctx: _Ctx,
    # Options
    name: str,
    styles: tuple[str, ...],
    dpi: int,
    start: int,
    stop: int,
    # Flags
    residual: bool,
    progress: bool,
    force: bool,
    verbose: bool,
    fail_fast: bool,
):
    def plot_func(ctx: _Ctx, subdir: SubDir) -> None:
        utils._balmer_templates(
            ctx=ctx,
            subdir=subdir,
            name=name,
            dpi=dpi,
            residual=residual,
            verbose=verbose & (not progress),
            force=force,
        )

    utils._plot_spectra_helper(
        ctx=ctx,
        plot_func=plot_func,
        styles=styles,
        start=start,
        stop=stop,
        progress=progress,
        verbose=verbose,
        fail_fast=fail_fast,
    )

def _host_templates(
    *,
    ctx: _Ctx,
    # Options
    name: str,
    styles: tuple[str, ...],
    dpi: int,
    start: int,
    stop: int,
    # Flags
    residual: bool,
    progress: bool,
    force: bool,
    verbose: bool,
    fail_fast: bool,
):
    def plot_func(ctx: _Ctx, subdir: SubDir) -> None:
        utils._host_templates(
            ctx=ctx,
            subdir=subdir,
            name=name,
            dpi=dpi,
            residual=residual,
            verbose=verbose & (not progress),
            force=force,
        )

    utils._plot_spectra_helper(
        ctx=ctx,
        plot_func=plot_func,
        styles=styles,
        start=start,
        stop=stop,
        progress=progress,
        verbose=verbose,
        fail_fast=fail_fast,
    )