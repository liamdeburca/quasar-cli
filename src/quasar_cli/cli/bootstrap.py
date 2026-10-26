from pathlib import Path

import click
from quasar_typing.literals import Variant
from quasar_typing.string_selections import DataTypes, ModelTypes

from quasar_cli.cli.context import _Ctx
from quasar_cli.utils import _map


def _bootstrap_validate_context(ctx: _Ctx) -> None:
    """Validate that the context is properly set prior to bootstrapping."""
    with ctx:
        assert "output_dir" in ctx


def _check_error_result_path(error_result_path: Path, verbose: bool, force: bool) -> None:
    error_result_path.parent.mkdir(parents=True, exist_ok=True)
    if error_result_path.exists() and not force:
        msg = f"Error result already exists at {error_result_path!s}! "\
            "Use '-f' or '--force' to overwrite."
        if verbose:
            click.echo(msg)
        raise FileExistsError(msg)

def _bootstrap_helper(
    *,
    ctx: _Ctx,
    variant: Variant,
    # Options
    model_types: set[ModelTypes] | None,
    data_types: set[DataTypes] | None,
    start: int,
    stop: int,
    # Flags
    progress: bool,
    verbose: bool,
    force: bool,
    fail_fast: bool,
) -> None:
    """
    Notes
    -----
    This function does not update the 'error_results' attribute of the context.
    This must instead be set by the `analysis init` command. 
    """
    from quasar_utils.pipeline import SubDir

    with ctx:
        output_dir = ctx.output_dir
        output_path = output_dir.path

        if verbose:
            click.echo(f"Bootstrapping for output path: {output_path!s}")
            click.echo(f"> Variant: {variant}")
            click.echo(f"> Model types: {model_types}")
            click.echo(f"> Data types: {data_types}")
            click.echo(f"> Progress: {progress}")
            click.echo(f"> Verbose: {verbose}")
            click.echo(f"> Force: {force}")

        _verbose = verbose and not progress
        subdirs = list(output_dir)

        msgs: list[str] = ["Failed to bootstrap spectra:"]
        def func(i: int, subdir: SubDir) -> None:
            key = subdir.in_file.stem
            error_result_path = ctx.error_results._get_path(key)
            _check_error_result_path(error_result_path, _verbose, force)

            spectrum = ctx.spectra[key]
            if _verbose: 
                click.echo(f"Bootstrapping from: {spectrum.title}")

            with subdir:
                try:
                    bootstrapper = spectrum.instantiateBootstrapper(
                        variant=variant,
                        model_types=model_types,
                        data_types=data_types,
                        tqdm_disable=progress & (variant != "spectrum"),
                        tqdm_leave=False,
                    )
                except Exception as exc:
                    msg: str = f"[INIT] {subdir.in_file.stem}: {i=}, {exc=}"
                    msgs.append(f"> {msg}")
                    if fail_fast:
                        raise ValueError(msg) from exc
                    return

                try:
                    samples = bootstrapper.run()
                except Exception as exc:
                    msg: str = f"[RUN] {subdir.in_file.stem}: {i=}, {exc=}"
                    msgs.append(f"> {msg}")
                    if fail_fast:
                        raise ValueError(msg) from exc
                    return
                
                try:
                    error_result = bootstrapper.toErrorResult(samples)
                except Exception as exc:
                    msg: str = f"[ERROR RESULT] {subdir.in_file.stem}: {i=}, {exc=}"
                    msgs.append(f"> {msg}")
                    if fail_fast:
                        raise ValueError(msg) from exc
                    return

                ctx.error_results[key] = error_result

        def desc_func(subdir: SubDir) -> str:
            return subdir.in_file.stem

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

def _spectrum_bootstrap(
    ctx: _Ctx,
    # Options
    mtypes: tuple[str, ...],
    dtypes: tuple[str, ...],
    start: int,
    stop: int,
    # Flags
    progress: bool,
    verbose: bool,
    force: bool,
    fail_fast: bool,
) -> None:
    _bootstrap_helper(
        ctx=ctx,
        variant="spectrum",
        model_types=ModelTypes(mtypes) or None,
        data_types=DataTypes(dtypes) or None,
        start=start,
        stop=stop,
        progress=progress,
        verbose=verbose,
        force=force,
        fail_fast=fail_fast,
    )


def _standard_bootstrap(
    ctx: _Ctx,
    # Options
    mtypes: tuple[str, ...] | None,
    dtypes: tuple[str, ...] | None,
    start: int,
    stop: int,
    # Flags
    progress: bool,
    verbose: bool,
    force: bool,
    fail_fast: bool,
):
    _bootstrap_helper(
        ctx=ctx,
        variant="standard",
        model_types=ModelTypes(mtypes) or None,
        data_types=DataTypes(dtypes) or None,
        start=start,
        stop=stop,
        progress=progress,
        verbose=verbose,
        force=force,
        fail_fast=fail_fast,
    )

