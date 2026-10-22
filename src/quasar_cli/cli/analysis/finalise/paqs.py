from collections import defaultdict
from typing import ClassVar

from numpy import (
    bool_,
    float32,
    float64,
    int32,
    int64,
    str_,
)

from quasar_cli.cli.context import _Ctx

from .utils import _cen_and_std


class _PAQSConfig:
    """
    Collection of metadata for outputting to PAQS format.
    """
    LINE_NAMES: ClassVar[list[str]] = ["LYA", "CIV", "MgII", "HB", "O5007", "HA"]
    
    MEASURE_NAMES: ClassVar[list[str]] = [
        "CEN_REST", "CEN_OBS", "CEN_OBS_ERR",
        "FLUX", "FLUX_ERR",
        "FWHM", "FWHM_ERR",
        "EW", "EW_ERR",
        "LDISP","LDISP_ERR",
        "FLUX_BROAD", "FLUX_BROAD_ERR",
        "FWHM_BROAD", "FWHM_BROAD_ERR",
        "FLUX_NARROW", "FLUX_NARROW_ERR",
        "FWHM_NARROW", "FWHM_NARROW_ERR",
    ]

    MEASURE_UNITS: ClassVar[list[str]] = [
        "angstrom", "angstrom", "angstrom",
        "erg/s/cm2", "erg/s/cm2",
        "km/s", "km/s",
        "erg/s/cm2", "erg/s/cm2",
        "km/s", "km/s",
        "erg/s/cm2", "erg/s/cm2",
        "km/s", "km/s",
        "erg/s/cm2", "erg/s/cm2",
        "km/s", "km/s",
    ]

    MEASURE_DATETYPES: ClassVar[list[str]] = [
        "D", "D", "D",
        "E", "E",
        "E", "E",
        "E", "E",
        "E", "E",
        "E", "E",
        "E", "E",
        "E", "E",
    ]

    @classmethod
    def get_names(cls) -> list[str]:
        return [
            f"{line}_{measure}"
            for line in cls.LINE_NAMES
            for measure in cls.MEASURE_NAMES
        ]

    @classmethod
    def is_observed(cls, name: str) -> bool:
        return "OBS" in name

    @classmethod
    def is_error(cls, name: str) -> bool:
        return "ERR" in name

    @classmethod
    def get_fits_datatype(cls, name: str) -> str:
        return "D" if "CEN" in name else "E"

    @classmethod
    def get_numpy_datatype(cls, name: str) -> str:
        return {
            "E": float32,
            "D": float64,
            "I": int32,
            "K": int64,
            "L": bool_,
            "A": str_,
        }.get(cls.get_fits_datatype(name))    

    @classmethod
    def get_measure_unit(cls, name: str) -> str:
        if ("_CEN" in name):
            return "angstrom"
        if ("_FLUX" in name) or ("_EW" in name):
            return "erg/s/cm2"
        if ("_FWHM" in name) or ("_LDISP" in name):
            return "km/s"

def _finalise_paqs(ctx: _Ctx) -> None:

    meta: dict[str, (str, str)] = {
        f"{line_name}_{measure_name}": (unit, datatype)
        for line_name in _PAQSConfig.LINE_NAMES
        for measure_name, unit, datatype in zip(
            _PAQSConfig.MEASURE_NAMES, 
            _PAQSConfig.MEASURE_UNITS,
            _PAQSConfig.MEASURE_DATETYPES,
        )
    }

    out: dict[str, list[float]] = defaultdict(list)
    for uid, result in ctx.results.items():
        out["uid"].append(uid)

        for name, (unit, datatype) in meta.items():
            if name not in result:
                out[name].append(None)
                continue

            dtype = float64 if datatype == "D" else float32
            res = result[name].to(unit)
            val = res.val.astype(dtype)
            unc = res.unc.astype(dtype)

            cen, std = _cen_and_std(val, unc)
            out[name].append(std if _PAQSConfig.is_error(name) else cen)
