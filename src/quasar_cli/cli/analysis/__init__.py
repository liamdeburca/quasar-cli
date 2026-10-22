import pickle

import click
from quasar_errors.analysis import Analyser
from quasar_errors.error_result import ErrorResult
from quasar_utils.pipeline import SubDir

from quasar_cli.cli.context import _Ctx
from quasar_cli.utils import _map

from .utils import _interval_helper, _target_helper


def _analysis_validate_context(ctx: _Ctx) -> None:
    """Validate that the context is properly set prior to analysis."""
    with ctx:
        assert "output_dir" in ctx


def _analysis_init(
    ctx: _Ctx,
    start: int,
    stop: int,
    verbose: bool,
    progress: bool,
    force: bool,
    fail_fast: bool,
) -> None:
    """
    Load the following into context:
    - Error results. 
    """
    with ctx:
        output_dir = ctx.output_dir

        # Error results
        if "error_results" in ctx:
            if not force:
                msg = "Found existing error results in context. Use '-f' or '--force' to overwrite."
                if verbose:
                    click.echo(f"> {msg}")
                raise RuntimeError(msg)
            ctx.remove("error_results")

        if "analysers" in ctx:
            if not force:
                msg = "Found existing analysers in context. Use '-f' or '--force' to overwrite."
                if verbose:
                    click.echo(f"> {msg}")
                raise RuntimeError(msg)
            ctx.remove("analysers")

        # Base error results
        msgs = ["Failed to load error results:"]
        error_results: dict[str, ErrorResult] = {}
        def func(idx, subdir: SubDir) -> None:
            with subdir:
                p = subdir._out_dir / "line_results/error_result.pkl"
                try:
                    with open(p, "rb") as f:
                        error_result = pickle.load(f)
                    error_results[subdir.in_file.stem] = error_result
                except Exception as exc:
                    msgs.append(f"> {subdir.in_file.stem}: {idx=}, {exc=}")
                    if fail_fast:
                        click.echo("\n".join(msgs))
                        raise
                    return
                    
        _map(
            func, output_dir, 
            start=start, 
            stop=stop, 
            progress=progress, 
            desc_func=lambda s: s.in_file.stem,
        )
        if error_results:
            ctx.error_results = error_results

        if verbose and len(msgs) > 1:
            click.echo("\n".join(msgs))


def _analysis_exit(ctx: _Ctx) -> None:
    """
    Clear the following attributes:
    - `error_results`
    - `analysers`
    """
    with ctx:
        if "error_results" in ctx:
            ctx.remove("error_results")
        if "analysers" in ctx:
            ctx.remove("analysers")


def _analysis_isolate(
    ctx: _Ctx,
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
    """
    Isolate existing error result based on the specified target pattern, line, 
    and wave. Then create `Analyser` instances.
    """
    with ctx:
        if verbose:
            click.echo("Isolating error results:")

        ### Fields that should exist

        if "config" not in ctx:
            msg = "No config found in context."
            if verbose:
                click.echo(f"> {msg}")
            raise RuntimeError(msg)
        
        if "error_results" not in ctx:
            msg = "No error results found in context."
            if verbose:
                click.echo(f"> {msg}")
            raise RuntimeError(msg)

        if "analysers" in ctx:
            if not force:
                msg = "Existing analysers found in context. Use -f or --force to overwrite."
                if verbose:
                    click.echo(f"> {msg}")
                raise RuntimeError(msg)
            ctx.remove("analysers")

        ### Isolate error results

        if verbose:
            click.echo(f"> Parsing: {pattern=}, {line=}, {wave=}")
        pattern, line, wave = _target_helper(
            pattern, 
            line, 
            wave, 
            verbose,
        )
        if verbose:
            click.echo(f"> Using: {pattern=}, {line=}, {wave=}")

        ers = {}
        msgs: list[str] = ["Failed to isolate:"]
        def func(i: int, item: tuple[str, ErrorResult]) -> None:
            key, er = item
            try:
                ers[key] = er.isolate(
                    target_pattern=pattern,
                    target_line=line,
                    target_wave=wave,
                )
            except Exception as exc:
                msgs.append(f"> {key}: {i=}, {exc=}")
                if fail_fast:
                    click.echo("\n".join(msgs))
                    raise
                return

        # Iterate over base error results
        it = list(ctx.error_results.items())
        _map(
            func, it, 
            start=0, 
            stop=-1, # Include entire range
            progress=progress,
            desc_func=lambda tup: tup[0],
            leave=False, # This should be fast, so no reason to keep bar
        )
        if verbose and len(msgs) > 1:
            click.echo("\n".join(msgs))

        ### Instantiate analysers from isolated error results

        if verbose:
            click.echo(f"> Parsing: {v_int=}, {ipv_int=}, {dx_int=}")
        v_int, ipv_int, dx_int = _interval_helper(
            ctx.config, v_int, ipv_int, dx_int, verbose,
        )
        if verbose:
            click.echo(f"> Using: {v_int=}, {ipv_int=}, {dx_int=}")

        msgs: list[str] = ["Failed to instantiate analysers:"]
        analysers: dict[str, Analyser] = {}
        def func(i: int, item: tuple[str, ErrorResult]) -> None:
            key, er = item
            try:
                analysers[key] = Analyser(
                    er,
                    info=ctx.config,
                    v_int=v_int,
                    ipv_int=ipv_int,
                    dx_int=dx_int,
                )
            except Exception as exc:
                msgs.append(f"> {key}: {i=}, {exc=}")
                if fail_fast:
                    click.echo("\n".join(msgs))
                    raise
                return

        def desc_func(item: tuple[str, ErrorResult]) -> str:
            return item[0]

        # Iterate over isolated error results
        it = list(ers.items())
        _map(
            func, it, 
            start=0, 
            stop=-1, # Include entire range
            progress=progress,
            desc_func=desc_func,
            leave=False, # This should be fast, so no reason to keep bar
        )
        ctx.analysers = analysers

        if verbose and len(msgs) > 1:
            click.echo("\n".join(msgs))
