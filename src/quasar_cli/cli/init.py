import click

from quasar_cli.cli.context import _Ctx


def _init(
    ctx: _Ctx,
    config: str,
    linelist: str,
    # Flags
    verbose: bool,
    force: bool,
    fail_fast: bool,
) -> None:
    """
    Initialize the context: open the context and set the fields manually. 
    """
    with ctx:
        if verbose:
            click.echo(f"Initializing context @ {ctx.path!s}")

        # CONFIG
        if "config" in ctx:
            if not force:
                msg = "Config already exists!"
                if fail_fast:
                    raise ValueError(msg)
                if verbose:
                    click.echo(f"> {msg} Use -f/--force to overwrite.")
            ctx.remove("config")
        else:
            ctx.config = config
            if verbose:
                click.echo("> Config set!")

        # LINELIST
        if "linelist" in ctx:
            if not force:
                msg = "Linelist already exists!"
                if fail_fast:
                    raise ValueError(msg)
                if verbose:
                    click.echo(f"> {msg} Use -f/--force to overwrite.")
            ctx.remove("linelist")
        else:
            ctx.linelist = linelist
            if verbose:
                click.echo("> Linelist set!")

        # FINALIZE
        if verbose:
            click.echo("Context initialization complete!")