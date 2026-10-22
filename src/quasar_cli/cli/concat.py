"""
CONCAT
------
Create a directory of symbolic links to specified files in an output directory.
"""
from os import symlink
from pathlib import Path

import click
from quasar_utils.pipeline import SubDir

from quasar_cli.cli.context import _Ctx
from quasar_cli.utils import _map


def _concat_helper(
    *,
    ctx: _Ctx,
    fname: str,
    start: int,
    stop: int,
    # Flags
    progress: bool,
    verbose: bool,
    force: bool,
    fail_fast: bool,
) -> None:
    with ctx:
        output_dir = ctx.output_dir
        output_path = output_dir.path
        workspace: Path = Path.cwd()

        if verbose:
            click.echo(f"Concatenating files for: {fname=}")
            click.echo(f"> Using output path: {output_path!s}")
            click.echo(f"> Using workspace path: {workspace!s}")

        subdirs = list(output_dir)
        if verbose:
            click.echo(f"> Found {len(subdirs)} subdirectories!")

        concatenation = workspace / Path(fname).stem
        if concatenation.exists() and not force:
            if verbose:
                click.echo(f"> Concatenation already exists: {concatenation!s}")
            raise FileExistsError(concatenation) 

        if verbose:
            click.echo(f"> Creating concatenation at: {concatenation!s}")
            click.echo(f"> Starting from index: {start}")
            if stop >= 0:
                click.echo(f"> Stopping at index: {stop}")
        
        concatenation.mkdir(exist_ok=True)

        msgs = ["Failed to concatentate:"]
        def func(i: int, subdir: SubDir) -> None:
            src = subdir._out_dir / "plots" / fname
            if not src.exists():
                msgs.append(f"> Source does not exist: {src!s}")
                if fail_fast:
                    raise FileNotFoundError(src)
                return
            
            dst = concatenation / (subdir.in_file.stem + src.suffix)
            if dst.exists() and not force:
                msgs.append(f"> Destination already exists: {dst!s}")
                if fail_fast:
                    raise FileExistsError(dst)
                return

            dst.unlink(missing_ok=True)
            symlink(src, dst)

        def desc_func(subdir: SubDir) -> str:
            return subdir.in_file.stem

        _map(
            func, subdirs,
            start=start,
            stop=stop,
            progress=progress,
            desc_func=desc_func,
            leave=False, # This is very fast, so no reason to leave progress bar
        )
        if verbose and len(msgs) > 1:
            click.echo("\n".join(msgs))


def _concat(
    *,
    ctx: _Ctx,
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
    for _fname in fname:
        _concat_helper(
            ctx=ctx,
            fname=_fname,
            start=start,
            stop=stop,
            progress=progress,
            verbose=verbose,
            force=force,
            fail_fast=fail_fast,
        )