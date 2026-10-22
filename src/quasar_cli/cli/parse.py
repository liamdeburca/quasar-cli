from pathlib import Path

import click
from quasar_utils.linelist import LineList
from quasar_utils.setup import Info


def _parse_linelist(
    linelist: str, 
    config: str, 
    verbose: bool,
) -> None:
    """
    Read the linelist using the given config file and write it to file again.
    """
    linelist = Path(linelist).resolve()
    config = Path(config).resolve()

    if verbose:
        click.echo(f"Parsing linelist file at: {linelist!s}")
        click.echo(f"> Using config file at: {config!s}")

    if not linelist.exists():
        if verbose:
            click.echo("> Linelist file does not exist!")
        raise FileNotFoundError(linelist)

    if not config.exists():
        if verbose:
            click.echo("> Config file does not exist!")
        raise FileNotFoundError(config)

    try:
        info: Info = Info.from_json(config)
    except Exception as e:
        if verbose:
            click.echo(f"> Failed to read config file with error: {e}")
        raise

    try:
        _linelist: LineList = LineList.read_csv(path=linelist, info=info)
    except Exception as e:
        if verbose:
            click.echo(f"> Failed to read linelist file with error: {e}")
        raise

    try:
        _linelist.to_csv(linelist)
    except Exception as e:
        if verbose:
            click.echo(f"> Failed to write linelist file with error: {e}")
        raise

    if verbose:
        click.echo("> Successfully parsed linelist file!")