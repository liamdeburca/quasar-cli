from collections.abc import Callable, Generator
from contextlib import contextmanager
from pathlib import Path

import click
from matplotlib.style import context
from quasar_utils.pipeline import SubDir

from quasar_cli.cli.context import _Ctx
from quasar_cli.utils import _map


@contextmanager
def _use_styles(
    styles: tuple[str, ...],
    verbose: bool,
) -> Generator[None, None, None]:
    """Context manager for temporarily applying matplotlib styles."""
    if "science" in styles:
        import scienceplots
        str(scienceplots)

    if verbose:
        if styles:
            click.echo(f"Using styles: {styles}")
        else:
            click.echo("Not using any styles!")

    if styles:
        _context = context(styles)
        _context.__enter__()
    yield None

    if styles:
        _context.__exit__(None, None, None)


def _check_plot_path(plot_path: Path, verbose: bool, force: bool) -> None:
    plot_path.parent.mkdir(parents=True, exist_ok=True)
    if plot_path.exists() and not force:
        msg = f"Plot already exists at {plot_path!s}! "\
            "Use '-f' or '--force' to overwrite."
        if verbose:
            click.echo(msg)
        raise FileExistsError(msg)

def _plot_spectra_helper(
    *,
    ctx: _Ctx,
    plot_func: Callable[[_Ctx, SubDir], None],

    styles: tuple[str, ...],
    start: int,
    stop: int,
    progress: int,
    verbose: bool,
    fail_fast: bool,
):
    with ctx, _use_styles(styles, verbose):
        msgs: list[str] = ["Failed to plot spectra:"]
        def func(i: int, subdir: SubDir) -> None:
            with subdir:
                try:
                    plot_func(ctx, subdir)
                except Exception as exc:
                    msgs.append(f"{subdir.in_file.stem}: {i=}, {exc=}")
                    if fail_fast:
                        raise

        def desc_func(subdir: SubDir) -> str:
            return subdir.in_file.stem

        subdirs = list(ctx.output_dir)
        _map(
            func, subdirs,
            start=start,
            stop=stop,
            progress=progress,
            desc_func=desc_func,
        )
        if verbose and len(msgs) > 1:
            click.echo("\n".join(msgs))

###

def _spectrum_quickplot(
    *,
    ctx: _Ctx,
    subdir: SubDir,
    name: str,
    dpi: int,
    verbose: bool,
    force: bool,
) -> None:
    plot_path = subdir.plots / name
    _check_plot_path(plot_path, verbose, force)

    spectrum = ctx.spectra[subdir]
    if verbose:
        click.echo(f"Making quickplot for: {spectrum.title}")

    return spectrum.quickplot()\
        .savefig(plot_path, dpi=dpi)\
        .close()


def _spectrum_differenceplot(
    *,
    ctx: _Ctx,
    subdir: SubDir,
    name: str,
    dpi: int,
    residual: bool,
    verbose: bool,
    force: bool
) -> None:
    plot_path = subdir.plots / name
    _check_plot_path(plot_path, verbose, force)
    
    spectrum = ctx.spectra[subdir]
    if verbose:
        click.echo(f"Making difference plot for: {spectrum.title}")

    return spectrum.differenceplot("residual" if residual else "difference")\
        .savefig(plot_path, dpi=dpi)\
        .close()

###

def _powerlaw_windows(
    *,
    ctx: _Ctx,
    subdir: SubDir,
    name: str,
    dpi: int,
    residual: bool,
    verbose: bool,
    force: bool  
) -> None:
    plot_path = subdir.plots / name
    _check_plot_path(plot_path, verbose, force)

    spectrum = ctx.spectra[subdir]
    if verbose:
        click.echo(f"Making powerlaw windows plot for: {spectrum.title}")

    if spectrum.pl and (n := len(spectrum.pl)) > 0:
        if verbose:
            click.echo(f"> {n} powerlaw windows available.")
        return spectrum.pl.windowsplot("residual" if residual else "difference")\
            .savefig(plot_path, dpi=dpi)\
            .close()

    if verbose:
        click.echo("> No powerlaw windows available.")

###

def _iron_windows(
    *,
    ctx: _Ctx,
    subdir: SubDir,
    name: str,
    dpi: int,
    residual: bool,
    verbose: bool,
    force: bool
) -> None:
    plot_path = subdir.plots / name
    _check_plot_path(plot_path, verbose, force)

    spectrum = ctx.spectra[subdir]
    if verbose:
        click.echo(f"Making iron windows plot for: {spectrum.title}")

    if spectrum.fe and (n := len(spectrum.fe)) > 0:
        if verbose:
            click.echo(f"> {n} iron windows available.")
        return spectrum.fe.windowsplot("residual" if residual else "difference")\
            .savefig(plot_path, dpi=dpi)\
            .close()

    if verbose:
        click.echo("> No iron windows available.")


def _iron_templates(
    *,
    ctx: _Ctx,
    subdir: SubDir,
    name: str,
    dpi: int,
    residual: bool,
    verbose: bool,
    force: bool
) -> None:
    plot_path = subdir.plots / name
    _check_plot_path(plot_path, verbose, force)

    spectrum = ctx.spectra[subdir]
    if verbose:
        click.echo(f"Making iron templates plot for: {spectrum.title}")

    if spectrum.fe and (n := len(spectrum.fe.template_models)) > 0:
        if verbose:
            click.echo(f"> {n} iron templates available.")
        return spectrum.fe.templatesplot("residual" if residual else "difference")\
            .savefig(plot_path, dpi=dpi)\
            .close()

    if verbose:
        click.echo("> No iron templates available.")

###

def _balmer_windows(
    *,
    ctx: _Ctx,
    subdir: SubDir,
    name: str,
    dpi: int,
    residual: bool,
    verbose: bool,
    force: bool
) -> None:
    plot_path = subdir.plots / name
    _check_plot_path(plot_path, verbose, force)

    spectrum = ctx.spectra[subdir]
    if verbose:
        click.echo(f"Making balmer windows plot for: {spectrum.title}")

    if spectrum.ba and (n := len(spectrum.ba)) > 0:
        if verbose:
            click.echo(f"> {n} balmer windows available.")
        return spectrum.ba.windowsplot("residual" if residual else "difference")\
            .savefig(plot_path, dpi=dpi)\
            .close()

    if verbose:
        click.echo("> No balmer windows available.")


def _balmer_templates(
    *,
    ctx: _Ctx,
    subdir: SubDir,
    name: str,
    dpi: int,
    residual: bool,
    verbose: bool,
    force: bool
) -> None:
    plot_path = subdir.plots / name
    _check_plot_path(plot_path, verbose, force)

    spectrum = ctx.spectra[subdir]
    if verbose:
        click.echo(f"Making balmer templates plot for: {spectrum.title}")

    if spectrum.ba and spectrum.ba.getModel() is not None:
        if verbose:
            click.echo("> Balmer model available.")
        return spectrum.ba.templatesplot("residual" if residual else "difference")\
            .savefig(plot_path, dpi=dpi)\
            .close()

    if verbose:
        click.echo("> No balmer model available.")

###

def _host_windows(
    *,
    ctx: _Ctx,
    subdir: SubDir,
    name: str,
    dpi: int,
    residual: bool,
    verbose: bool,
    force: bool
) -> None:
    plot_path = subdir.plots / name
    _check_plot_path(plot_path, verbose, force)

    spectrum = ctx.spectra[subdir]
    if verbose:
        click.echo(f"Making host windows plot for: {spectrum.title}")

    if spectrum.hg and (n := len(spectrum.hg)) > 0:
        if verbose:
            click.echo(f"> {n} host windows available.")
        return spectrum.hg.windowsplot("residual" if residual else "difference")\
            .savefig(plot_path, dpi=dpi)\
            .close()

    if verbose:
        click.echo("> No host windows available.")

def _host_templates(
    *,
    ctx: _Ctx,
    subdir: SubDir,
    name: str,
    dpi: int,
    residual: bool,
    verbose: bool,
    force: bool
) -> None:
    plot_path = subdir.plots / name
    _check_plot_path(plot_path, verbose, force)

    spectrum = ctx.spectra[subdir]
    if verbose:
        click.echo(f"Making host template plot for: {spectrum.title}")

    if spectrum.hg and spectrum.hg.getModel() is not None:
        if verbose:
            click.echo("> Host Galaxy model available.")
        return spectrum.hg.templatesplot("residual" if residual else "difference")\
            .savefig(plot_path, dpi=dpi)\
            .close()

    if verbose:
        click.echo("> No host model available.")