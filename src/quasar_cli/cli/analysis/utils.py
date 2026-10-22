import click
from astropy.constants import c
from astropy.units import Unit
from quasar_utils.setup import Info


def _target_helper(
    pattern: tuple[str, ...],
    line: tuple[str, ...],
    wave: tuple[float, ...],
    verbose: bool,
) -> tuple[
    str | set[str] | None,
    str | set[str] | None,
    float | set[float] | None,
]:
    if not any([pattern, line, wave]):
        if verbose:
            click.echo("> No target pattern(s), line(s), or wave(s) provided.")
        return (None, None, None)

    if pattern:
        pattern = pattern[0] \
            if len(pattern) == 1 \
            else set(pattern)
        return (pattern, None, None)

    if line:
        line = line[0] \
            if len(line) == 1 \
            else set(line)
        return (None, line, None)

    if wave:
        wave = wave[0] \
            if len(wave) == 1 \
            else set(wave)
        return (None, None, wave)


def _interval_helper(
    config: Info,
    v_int: float,
    ipv_int: float,
    dx_int: float,
    verbose: bool,
) -> tuple[float, float, float]:
    if v_int == -1:
        v_int = config.error.v_int
        if verbose:
            click.echo(f"> No `v_int` provided. Using: {v_int=:.1f}")
    else:
        # 'km/s' to 'c'
        v_int /= c.to("km/s").value

    if ipv_int == -1:
        ipv_int = config.error.ipv_int
        if verbose:
            click.echo(f"> No `ipv_int` provided. Using: {ipv_int=:.1f}")        

    if dx_int == -1:
        dx_int = config.error.dx_int
        if verbose:
            click.echo(f"> No `dx_int` provided. Using: {dx_int=:.1f}")
    else:
        # 'angstrom' to unitless
        dx_int = config.units.getUnitlessWavelength(dx_int * Unit("angstrom"))

    if verbose:
        if v_int > 0:
            click.echo(
                "> Using velocity interval (`v_int`) for analysis: "
                f"v_int={v_int * c.to('km/s').value:.1e} (km/s)")
        elif ipv_int > 0:
            click.echo(
                "> Using IPV interval (`ipv_int`) for analysis: "
                f"{ipv_int=:.1f}"
            )
        if dx_int > 0:
            click.echo(
                "> Using wavelength interval (`dx_int`) for analysis: "
                f"dx_int={config.units.getWavelength(dx_int).value:.1f} angstrom"
            )

    return v_int, ipv_int, dx_int