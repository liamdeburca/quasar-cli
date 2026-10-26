from pathlib import Path

import click
from quasar_utils.pipeline import InputDir, OutputDir

from quasar_cli.cli.context import _Ctx
from quasar_cli.pipelines import SDSSPipeline


def _run_validate_context(ctx: _Ctx) -> None:
    """Checks that the context is ready!"""
    with ctx:
        assert "config" in ctx
        assert "linelist" in ctx

def _prepare_run(
    *,
    ctx: _Ctx,
    input_path: str | Path,
    output_path: str | Path,
    clear_existing: bool,
    verbose: bool,
) -> None:
    """
    Prepares the context for a run: sets the `input_dir` and `output_dir` 
    attributes.
    """
    input_path = Path(input_path).resolve()
    try:
        input_dir = InputDir.create(input_path)
        if verbose:
            click.echo(f"> Instantiated `InputDir` from: {input_path!s}")
    except Exception:
        if verbose:
            click.echo("> Failed to instantiate `InputDir`!")
        raise

    output_path = Path(output_path).resolve()
    try:
        output_dir = OutputDir.create(
            input_dir, 
            path=output_path,
            dangerous=clear_existing,
        )
        if verbose:
            click.echo(f"> Instantiated `OutputDir` at path: {output_dir.path!s}")
    except Exception:
        if verbose:
            click.echo("> Failed to instantiate `OutputDir`!")
        raise

    ctx.input_dir = input_dir
    ctx.output_dir = output_dir


def _run_sdss(
    ctx: _Ctx,
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
    """Run the SDSS pipeline on the spectra in the specified input directory."""

    if verbose:
        click.echo("Running SDSS pipeline...")

    with ctx:
        _prepare_run(
            ctx=ctx,
            input_path=input_path,
            output_path=output_path,
            clear_existing=clear_existing,
            verbose=verbose,
        )
        pipeline = SDSSPipeline(
            config=ctx.config,
            linelist=ctx.linelist,
            output_dir=ctx.output_dir,
            
            start=start,
            stop=stop,

            host_first=host_first,
            force=force,
            progress=progress,
            fail_fast=fail_fast,
        )
        spectra, msgs = pipeline.run()

        ctx.spectra.update(spectra)
        if verbose and len(msgs) > 1:
            click.echo("\n".join(msgs))
    