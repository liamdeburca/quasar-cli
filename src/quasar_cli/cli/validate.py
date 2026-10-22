from pathlib import Path

import click
from pydantic import ValidationError


def _validate_config(
    config: str, 
    verbose: bool,
) -> None:
    """Validate the config file at the specified path."""
    from quasar_utils.setup import Info
    
    path: Path = Path(config).resolve()

    if verbose:
        click.echo(f"Validating config file at: {path!s}")

    if not path.exists():
        if verbose:
            click.echo("[FAILED] Cannot find config file!")
        raise FileNotFoundError(path)

    try:
        Info.from_json(path)
    except (ValueError, ValidationError) as e:
        if verbose:
            click.echo(f"[FAILED] Failed to read config file with error: {e}")
        raise

    if verbose:
        click.echo("[SUCCESS] Config file is valid!")


def _validate_linelist(
    linelist: str, 
    verbose: bool,
) -> None:
    """Validate the linelist file at the specified path using the given config."""
    from quasar_utils.linelist import LineList
    from quasar_utils.setup import Info

    path: Path = Path(linelist).resolve()

    if verbose:
        click.echo(f"Validating linelist file at: {path!s}")

    if not path.exists():
        if verbose:
            click.echo("[FAILED] Cannot find linelist file!")
        raise FileNotFoundError(path)

    info: Info = Info()

    try:
        LineList.read_csv(path=path, info=info)
    except (ValueError, ValidationError) as e:
        if verbose:
            click.echo(f"[FAILED] Failed to read linelist file with error: {e}")
        raise

    if verbose:
        click.echo("[SUCCESS] Linelist file is valid!")


def _validate_lookup(
    lookup: str,
    verbose: bool,
) -> None:
    """Validate the lookup file at the specified path."""
    path: Path = Path(lookup).resolve()

    if verbose:
        click.echo(f"Validating lookup file at: {path!s}")

    if not path.exists():
        if verbose:
            click.echo("[FAILED] Lookup file is missing!")
        raise FileNotFoundError(path)

    if verbose:
        click.echo("[SUCCESS] Lookup file is valid!")


def _validate_workspace(
    workspace: str,
    verbose: bool,
) -> None:
    """Validate the workspace at the specified path."""
    path: Path = Path(workspace).resolve()
    config: Path = path / "config.json"
    linelist: Path = path / "linelist.csv"
    lookup: Path = path / "lookup.csv"

    if verbose:
        click.echo(f"Validating workspace at: {path!s}")

    _validate_config(config, verbose)
    _validate_linelist(linelist, verbose)
    _validate_lookup(lookup, verbose)

    if verbose:
        click.echo("[SUCCESS] Workspace is valid!")