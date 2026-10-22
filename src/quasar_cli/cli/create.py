from pathlib import Path
from shutil import copyfile

import click
from pydantic import ValidationError
from quasar_utils.setup import Info

from ..utils import DefaultPaths


def _create_config(
    config: str, 
    force: bool,
    verbose: bool,
) -> None:
    """Create a new config file (JSON) at the specified path."""
    path: Path = Path(config).resolve()

    if verbose:
        click.echo(f"Creating config file at: {path!s}")
    if path.exists() and not force:
        if verbose:
            click.echo("> File already exists! Use '-f' or '--force' to replace it.")
        raise FileExistsError(path)

    try:
        path.unlink(missing_ok=True)
        Info().to_json(path)
    except (ValueError, ValidationError) as e:
        if verbose:
            click.echo(f"> Failed to create config file with error: {e}")
        raise

    if verbose:
        click.echo(f"> Successfully created config file at {path!s}")


def _create_linelist(
    linelist: str, 
    force: bool,
    verbose: bool,
) -> None:
    """Create a new linelist file (CSV) at the specified path."""
    path: Path = Path(linelist).resolve()

    if verbose:
        click.echo(f"Creating linelist file at: {path!s}")
    if path.exists() and not force:
        if verbose:
            click.echo("> File already exists! Use '-f' or '--force' to replace it.")
        raise FileExistsError(path)

    try:
        path.unlink(missing_ok=True)
        copyfile(DefaultPaths.linelist, path)
    except ValueError as e:
        if verbose:
            click.echo(f"> Failed to copy linelist file with error: {e}")
        raise
    
    if verbose:
        click.echo(f"> Successfully created linelist file at {path!s}")


def _create_lookup(
    lookup: str, 
    force: bool,
    verbose: bool,
) -> None:
    """
    Create a new lookup file (CSV) at the specified path.
    """
    path: Path = Path(lookup).resolve()

    if verbose:
        click.echo(f"Creating lookup file at: {path!s}")
    if path.exists() and not force:
        if verbose:
            click.echo("> File already exists! Use '-f' or '--force' to replace it.")
        raise FileExistsError(path)

    try:
        path.unlink(missing_ok=True)
        copyfile(DefaultPaths.lookup, path)
    except ValueError as e:
        if verbose:
            click.echo(f"> Failed to copy lookup file with error: {e}")
        raise

    if verbose:
        click.echo(f"> Successfully created lookup file at {path!s}")


def _create_workspace(
    workspace: str, 
    force: bool,
    verbose: bool,
) -> None:
    """
    Create a new workspace directory with default config (JSON), linelist (CSV), 
    and lookup (CSV) files.
    """
    path: Path = Path(workspace).resolve()

    if verbose:
        click.echo(f"Creating workspace at: {path!s}")
    if path.suffix != "":
        if verbose:
            click.echo("> Workspace path should be a directory, not a file.")
        raise NotADirectoryError(path)

    path.mkdir(parents=True, exist_ok=True)
    _create_config(path / "config.json", force, verbose)
    _create_linelist(path / "linelist.csv", force, verbose)
    _create_lookup(path / "lookup.csv", force, verbose)

    if verbose:
        click.echo(f"> Successfully created all necessary files in workspace at {path!s}")
        click.echo(f"> Run `cd {path!s}` to enter the workspace")
