import click

from quasar_cli.cli.arguments import (
    AnyPathArguments,
    Arguments,
    MeasureArguments,
    PathArguments,
)
from quasar_cli.cli.flags import Flags, MeasureFlags, PlotFlags
from quasar_cli.cli.options import (
    AnalysisOptions,
    BootstrapOptions,
    MeasureOptions,
    Options,
    PlotOptions,
)


@click.group()
@click.pass_context
def cli(context: click.Context):
    """Ensure that a context object is set."""
    from quasar_cli.cli.context import _Ctx
    context.ensure_object(_Ctx)


@cli.command("init")
@Options.chain("config", "linelist")
@Flags.chain("verbose", "force", "fail_fast")
@click.pass_obj
def cli_init(
    ctx: object,
    config: str,
    linelist: str,
    verbose: bool,
    force: bool,
    fail_fast: bool
):
    from .init import _init
    _init(ctx, config, linelist, verbose, force, fail_fast)


@cli.command("describe-context")
@click.pass_obj
def cli_describe_context(ctx: object):
    from quasar_cli.cli.context import _describe_context
    _describe_context(ctx)

### Create

@cli.group()
def create():
    pass

@create.command("config")
@AnyPathArguments.config()
@Flags.chain("force", "verbose")
def cli_create_config(config: str, force: bool, verbose: bool) -> None:
    from .create import _create_config
    _create_config(config, force, verbose)


@create.command("linelist")
@AnyPathArguments.linelist()
@Flags.chain("force", "verbose")
def cli_create_linelist(linelist: str, force: bool, verbose: bool) -> None:
    from .create import _create_linelist
    _create_linelist(linelist, force, verbose)


@create.command("lookup")
@AnyPathArguments.lookup()
@Flags.chain("force", "verbose")
def cli_create_lookup(lookup: str, force: bool, verbose: bool) -> None:
    from .create import _create_lookup
    _create_lookup(lookup, force, verbose)


@create.command("workspace")
@AnyPathArguments.workspace()
@Flags.chain("force", "verbose")
def cli_create_workspace(workspace: str, force: bool, verbose: bool) -> None:
    from .create import _create_workspace
    _create_workspace(workspace, force, verbose)

### Validation

@cli.group()
def validate():
    pass

@validate.command("config")
@PathArguments.config()
@Flags.verbose()
def cli_validate_config(config: str, verbose: bool) -> None:
    from .validate import _validate_config
    _validate_config(config, verbose)


@validate.command("linelist")
@PathArguments.linelist()
@Flags.verbose()
def cli_validate_linelist(linelist: str, verbose: bool) -> None:
    from .validate import _validate_linelist
    _validate_linelist(linelist, verbose)


@validate.command("lookup")
@PathArguments.lookup()
@Flags.verbose()
def cli_validate_lookup(lookup: str, verbose: bool) -> None:
    from .validate import _validate_lookup
    _validate_lookup(lookup, verbose)


@validate.command("workspace")
@PathArguments.workspace()
@Flags.verbose()
def cli_validate_workspace(workspace: str, verbose: bool) -> None:
    from .validate import _validate_workspace
    _validate_workspace(workspace, verbose)

### Parsing

@cli.group()
def parse():
    pass

@parse.command("linelist")
@PathArguments.linelist()
@Options.config()
@Flags.verbose()
def cli_parse_linelist(linelist: str, config: str, verbose: bool) -> None:
    from .parse import _parse_linelist
    _parse_linelist(linelist, config, verbose)

### Running the pipeline

@cli.group()
@click.pass_obj
def run(ctx: object):
    """Validate that the context object is ready."""
    # runtime validation will be performed by the concrete run commands

@run.command("sdss")
@PathArguments.input_path()
@Options.chain("output_path", "start", "stop")
@Flags.chain(
    "clear_existing", "host_first", "force", "verbose", "progress", "fail_fast"
)
@click.pass_obj
def run_sdss(
    ctx: object,
    input_path: str,
    # Options
    output_path: str,
    start: int,
    stop: int,
    # Flags
    clear_existing: bool,
    host_first: bool,
    force: bool,
    verbose: bool,
    progress: bool,
    fail_fast: bool,
) -> None:
    from .run import _run_sdss
    _run_sdss(
        ctx=ctx,
        input_path=input_path,
        output_path=output_path,
        start=start,
        stop=stop,
        clear_existing=clear_existing,
        host_first=host_first,
        force=force,
        verbose=verbose,
        progress=progress,
        fail_fast=fail_fast,
    )

@run.command("paqs")
@PathArguments.input_path()
@Options.chain("output_path", "start", "stop")
@Flags.chain(
    "clear_existing", "host_first", "force", "verbose", "progress", "fail_fast"
)
@click.pass_obj
def run_paqs(
    ctx: object,
    input_path: str,
    # Options
    output_path: str,
    start: int,
    stop: int,
    # Flags
    clear_existing: bool,
    host_first: bool,
    force: bool,
    verbose: bool,
    progress: bool,
    fail_fast: bool,
) -> None:
    # Not implemented: delegate to implementation if/when added
    raise NotImplementedError()


### Plotting

@cli.group()
@click.pass_obj
def plot(ctx: object):
    # validation will be performed by the concrete plot command implementation
    # which we import lazily when the command runs.
    pass

@plot.group()
def spectrum():
    pass


@spectrum.command("quick")
@PlotOptions.name(default="quick.png")
@PlotOptions.chain("styles", "dpi")
@Options.chain("start", "stop")
@Flags.chain("progress", "force", "verbose", "fail_fast")
@click.pass_obj
def cli_spectrum_quick(
    ctx: object,
    name: str,
    styles: tuple[str, ...],
    dpi: int,
    start: int,
    stop: int,
    progress: bool,
    force: bool,
    verbose: bool,
    fail_fast: bool,
):
    from .plot import _spectrum_quick
    _spectrum_quick(
        ctx=ctx,
        name=name,
        styles=styles,
        dpi=dpi,
        start=start,
        stop=stop,
        progress=progress,
        force=force,
        verbose=verbose,
        fail_fast=fail_fast,
    )


@spectrum.command("difference")
@PlotOptions.name(default="difference.png")
@PlotOptions.chain("styles", "dpi")
@Options.chain("start", "stop")
@PlotFlags.residual()
@Flags.chain("progress", "force", "verbose", "fail_fast")
@click.pass_obj
def cli_spectrum_difference(
    ctx: object,
    name: str,
    styles: tuple[str, ...],
    dpi: int,
    start: int,
    stop: int,
    residual: bool,
    progress: bool,
    force: bool,
    verbose: bool,
    fail_fast: bool,
):
    from .plot import _spectrum_difference
    _spectrum_difference(
        ctx=ctx,
        name=name,
        styles=styles,
        dpi=dpi,
        start=start,
        stop=stop,
        residual=residual,
        progress=progress,
        force=force,
        verbose=verbose,
        fail_fast=fail_fast,
    )


@spectrum.command("windows-pl")
@PlotOptions.name(default="windows_pl.png")
@PlotOptions.chain("styles", "dpi")
@Options.chain("start", "stop")
@PlotFlags.residual()
@Flags.chain("progress", "force", "verbose", "fail_fast")
@click.pass_obj
def cli_powerlaw_windows(
    ctx: object,
    name: str,
    styles: tuple[str, ...],
    dpi: int,
    start: int,
    stop: int,
    residual: bool,
    progress: bool,
    force: bool,
    verbose: bool,
    fail_fast: bool,
):
    from .plot import _powerlaw_windows
    _powerlaw_windows(
        ctx=ctx,
        name=name,
        styles=styles,
        dpi=dpi,
        start=start,
        stop=stop,
        residual=residual,
        progress=progress,
        force=force,
        verbose=verbose,
        fail_fast=fail_fast,
    )


@spectrum.command("windows-fe")
@PlotOptions.name(default="windows_fe.png")
@PlotOptions.chain("styles", "dpi")
@Options.chain("start", "stop")
@PlotFlags.residual()
@Flags.chain("progress", "force", "verbose", "fail_fast")
@click.pass_obj
def cli_iron_windows(
    ctx: object,
    name: str,
    styles: tuple[str, ...],
    dpi: int,
    start: int,
    stop: int,
    residual: bool,
    progress: bool,
    force: bool,
    verbose: bool,
    fail_fast: bool,
):
    from .plot import _iron_windows
    _iron_windows(
        ctx=ctx,
        name=name,
        styles=styles,
        dpi=dpi,
        start=start,
        stop=stop,
        residual=residual,
        progress=progress,
        force=force,
        verbose=verbose,
        fail_fast=fail_fast,
    )


@spectrum.command("windows-ba")
@PlotOptions.name(default="windows_ba.png")
@PlotOptions.chain("styles", "dpi")
@Options.chain("start", "stop")
@PlotFlags.residual()
@Flags.chain("progress", "force", "verbose", "fail_fast")
@click.pass_obj
def cli_balmer_windows(
    ctx: object,
    name: str,
    styles: tuple[str, ...],
    dpi: int,
    start: int,
    stop: int,
    residual: bool,
    progress: bool,
    force: bool,
    verbose: bool,
    fail_fast: bool,
):
    from .plot import _balmer_windows
    _balmer_windows(
        ctx=ctx,
        name=name,
        styles=styles,
        dpi=dpi,
        start=start,
        stop=stop,
        residual=residual,
        progress=progress,
        force=force,
        verbose=verbose,
        fail_fast=fail_fast,
    )


@spectrum.command("windows-hg")
@PlotOptions.name(default="windows_hg.png")
@PlotOptions.chain("styles", "dpi")
@Options.chain("start", "stop")
@PlotFlags.residual()
@Flags.chain("progress", "force", "verbose", "fail_fast")
@click.pass_obj
def cli_host_windows(
    ctx: object,
    name: str,
    styles: tuple[str, ...],
    dpi: int,
    start: int,
    stop: int,
    residual: bool,
    progress: bool,
    force: bool,
    verbose: bool,
    fail_fast: bool,
):
    from .plot import _host_windows
    _host_windows(
        ctx=ctx,
        name=name,
        styles=styles,
        dpi=dpi,
        start=start,
        stop=stop,
        residual=residual,
        progress=progress,
        force=force,
        verbose=verbose,
        fail_fast=fail_fast,
    )


@spectrum.command("templates-fe")
@PlotOptions.name(default="templates_fe.png")
@PlotOptions.chain("styles", "dpi")
@Options.chain("start", "stop")
@PlotFlags.residual()
@Flags.chain("progress", "force", "verbose", "fail_fast")
@click.pass_obj
def cli_iron_templates(
    ctx: object,
    name: str,
    styles: tuple[str, ...],
    dpi: int,
    start: int,
    stop: int,
    residual: bool,
    progress: bool,
    force: bool,
    verbose: bool,
    fail_fast: bool,
):
    from .plot import _iron_templates
    _iron_templates(
        ctx=ctx,
        name=name,
        styles=styles,
        dpi=dpi,
        start=start,
        stop=stop,
        residual=residual,
        progress=progress,
        force=force,
        verbose=verbose,
        fail_fast=fail_fast,
    )


@spectrum.command("templates-ba")
@PlotOptions.name(default="templates_balmer.png")
@PlotOptions.chain("styles", "dpi")
@Options.chain("start", "stop")
@PlotFlags.residual()
@Flags.chain("progress", "force", "verbose", "fail_fast")
@click.pass_obj
def cli_balmer_templates(
    ctx: object,
    name: str,
    styles: tuple[str, ...],
    dpi: int,
    start: int,
    stop: int,
    residual: bool,
    progress: bool,
    force: bool,
    verbose: bool,
    fail_fast: bool,
):
    from .plot import _balmer_templates
    _balmer_templates(
        ctx=ctx,
        name=name,
        styles=styles,
        dpi=dpi,
        start=start,
        stop=stop,
        residual=residual,
        progress=progress,
        force=force,
        verbose=verbose,
        fail_fast=fail_fast,
    )


@spectrum.command("templates-hg")
@PlotOptions.name(default="templates_hg.png")
@PlotOptions.chain("styles", "dpi")
@Options.chain("start", "stop")
@PlotFlags.residual()
@Flags.chain("progress", "force", "verbose", "fail_fast")
@click.pass_obj
def cli_host_templates(
    ctx: object,
    name: str,
    styles: tuple[str, ...],
    dpi: int,
    start: int,
    stop: int,
    residual: bool,
    progress: bool,
    force: bool,
    verbose: bool,
    fail_fast: bool,
):
    from .plot import _host_templates
    _host_templates(
        ctx=ctx,
        name=name,
        styles=styles,
        dpi=dpi,
        start=start,
        stop=stop,
        residual=residual,
        progress=progress,
        force=force,
        verbose=verbose,
        fail_fast=fail_fast,
    )

### Bootstrapping

@cli.group()
@click.pass_obj
def bootstrap(ctx: object):
    # concrete implementations will validate the context lazily when run
    pass


@bootstrap.command("spectrum")
@BootstrapOptions.chain("model_types", "data_types")
@Options.chain("start", "stop")
@Flags.chain("progress", "verbose", "force", "fail_fast")
@click.pass_obj
def cli_spectrum_bootstrap(
    ctx: object,
    mtypes: tuple[str, ...],
    dtypes: tuple[str, ...],
    start: int,
    stop: int,
    progress: bool,
    verbose: bool,
    force: bool,
    fail_fast: bool,
) -> None:
    from .bootstrap import _spectrum_bootstrap
    _spectrum_bootstrap(
        ctx=ctx,
        mtypes=mtypes,
        dtypes=dtypes,
        start=start,
        stop=stop,
        progress=progress,
        verbose=verbose,
        force=force,
        fail_fast=fail_fast,
    )


@bootstrap.command("standard")
@BootstrapOptions.chain("model_types", "data_types")
@Options.chain("start", "stop")
@Flags.chain("progress", "verbose", "force", "fail_fast")
@click.pass_obj
def cli_standard_bootstrap(
    ctx: object,
    mtypes: tuple[str, ...] | None,
    dtypes: tuple[str, ...] | None,
    start: int,
    stop: int,
    progress: bool,
    verbose: bool,
    force: bool,
    fail_fast: bool,
) -> None:
    from .bootstrap import _standard_bootstrap
    _standard_bootstrap(
        ctx=ctx,
        mtypes=mtypes,
        dtypes=dtypes,
        start=start,
        stop=stop,
        progress=progress,
        verbose=verbose,
        force=force,
        fail_fast=fail_fast,
    )

### Analysis

@cli.group()
@click.pass_obj
def analysis(ctx: object):
    # validation will be performed by the concrete analysis commands
    pass


@analysis.command("init")
@Options.chain("start", "stop")
@Flags.chain("verbose", "progress", "force", "fail_fast")
@click.pass_obj
def cli_analysis_init(
    ctx: object,
    start: int,
    stop: int,
    verbose: bool,
    progress: bool,
    force: bool,
    fail_fast: bool,
) -> None:
    from .analysis import _analysis_init
    _analysis_init(
        ctx=ctx,
        start=start,
        stop=stop,
        verbose=verbose,
        progress=progress,
        force=force,
        fail_fast=fail_fast,
    )


@analysis.command("isolate")
@AnalysisOptions.chain("pattern", "line", "wave", "v_int", "ipv_int", "dx_int")
@Flags.chain("verbose", "progress", "force", "fail_fast")
@click.pass_obj
def cli_analysis_isolate(
    ctx: object,
    pattern: tuple[str, ...],
    line: tuple[str, ...],
    wave: tuple[float, ...],
    v_int: float,
    ipv_int: float,
    dx_int: float,
    verbose: bool,
    progress: bool,
    force: bool,
    fail_fast: bool,
) -> None:
    from .analysis import _analysis_isolate
    _analysis_isolate(
        ctx=ctx,
        pattern=pattern,
        line=line,
        wave=wave,
        v_int=v_int,
        ipv_int=ipv_int,
        dx_int=dx_int,
        verbose=verbose,
        progress=progress,
        force=force,
        fail_fast=fail_fast,
    )


@analysis.command("exit")
@click.pass_obj
def cli_analysis_exit(ctx: object) -> None:
    from .analysis import _analysis_exit
    _analysis_exit(ctx)


@analysis.group()
@click.pass_context
def measure(ctx: click.Context):
    pass

@measure.command("mode-off")
@MeasureArguments.name()
@MeasureOptions.chain("bg", "unit")
@MeasureFlags.from_model()
@Flags.chain("verbose", "force", "progress", "fail_fast")
@click.pass_obj
def measure_mode_off(
    ctx: object,
    name: str,
    bg: tuple[str, ...],
    unit: str,
    from_model: bool,
    verbose: bool,
    force: bool,
    progress: bool,
    fail_fast: bool,
) -> None:
    from .analysis.measure import _mode_off
    _mode_off(
        ctx=ctx,
        name=name,
        bg=bg,
        unit=unit,
        from_model=from_model,
        verbose=verbose,
        force=force,
        progress=progress,
        fail_fast=fail_fast,
    )


### Miscellaneous

@cli.command("concat")
@Arguments.fname(nargs=-1)
@Options.chain("start", "stop")
@Flags.chain("progress", "verbose", "force", "fail_fast")
@click.pass_obj
def concat(
    ctx: object,
    fname: str,
    # Options
    start: int,
    stop: int,
    # Flags
    progress: bool,
    verbose: bool,
    force: bool,
    fail_fast: bool,
) -> None:
    from .concat import _concat
    _concat(
        ctx=ctx,
        fname=fname,
        start=start,
        stop=stop,
        progress=progress,
        verbose=verbose,
        force=force,
        fail_fast=fail_fast,
    )

    
if __name__ == "__main__":
    cli()
