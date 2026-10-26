from typing import Literal


def _describe_context(ctx: object) -> None:
    """Describe the context."""
    from click import echo

    _validate_context(ctx)
    with ctx:
        echo("Current context:")

        if "config" in ctx:
            echo("> Config: Loaded!")
        else:
            echo("> Config: Not set!")

        if "linelist" in ctx:
            n = len(ctx.linelist.name)
            echo(f"> Linelist: {n} rows")
        else:
            echo("> Linelist: Not set!")

        if "input_dir" in ctx:
            n = len(ctx.input_dir.files)
            echo(f"> Input directory: {ctx.input_dir.path!s} w/ {n} spectra")
        else:
            echo("> Input directory: Not set!")
        
        if "output_dir" in ctx:
            n = len(ctx.output_dir)
            echo(f"> Output directory: {ctx.output_dir.path!s} w/ {n} subdirs")

            echo(f"> Spectra: {ctx.spectra.get_length(ctx.output_dir)} items")
            echo(f"> ErrorResults: {ctx.error_results.get_length(ctx.output_dir)} items")
            echo(f"> Analysers: {ctx.analysers.get_length(ctx.output_dir)} items")
            echo(f"> Results: {ctx.results.get_length(ctx.output_dir)} items")
        else:
            echo("> Output directory: Not set!")
            echo("> Spectra: Not set!")
            echo("> ErrorResults: Not set!")
            echo("> Analysers: Not set!")
            echo("> Results: Not set!")


def _validate_context(
    ctx: object,
    *required_fields: Literal["config", "linelist", "input_dir", "output_dir"],
) -> None:
    from .context import _Ctx

    if not isinstance(ctx, _Ctx):
        raise TypeError(
            "Context object must be an instance of '_Ctx', got "
            f"{type(ctx).__name__}"
        )

    with ctx:
        for field in required_fields:
            if field not in ctx:
                raise ValueError(f"Context is missing required field: '{field}'")
        
