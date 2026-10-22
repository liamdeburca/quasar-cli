from math import isfinite

from astropy.units import Unit
from quasar_typing.misc import BackgroundFlux

from quasar_cli.cli.context import _Ctx


def validate_bg_flux(bg_flux: tuple[str, ...]) -> BackgroundFlux | None:
    return BackgroundFlux(bg_flux) if bg_flux else None

def validate_unit(unit: str) -> str:
    _ = Unit(unit)
    return str(unit)

def validate_x_bounds(lb: float, ub: float) -> tuple[float, float]:
    assert isfinite(lb) and isfinite(ub)
    assert 0 <= lb
    assert lb < ub
    return float(lb), float(ub)

def validate_q(q: float) -> float:
    assert isfinite(q)
    assert 0 < q
    assert q < 1
    return float(q)

def validate_p(p: float) -> float:
    assert isfinite(p)
    assert 0 < p
    assert p < 100
    return float(p)

def validate_h(h: float) -> float:
    return validate_q(h) # Identical validation steps

def validate_name(
    ctx: _Ctx,
    name: str,
    force: bool,
) -> str:
    if ("results" not in ctx) or (name not in ctx.results):
        return name

    cols: set[str] = {
        k
        for result in ctx.results.values()
        for k in result
    }
    if name in cols and not force:
        msg = f"Result with name '{name}' already exists!"
        raise ValueError(msg)
    return name