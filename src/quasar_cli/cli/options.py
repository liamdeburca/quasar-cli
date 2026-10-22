
from collections.abc import Callable

from click import Option, Path, option

from .utils import BaseParameters


class Options(BaseParameters):
    @classmethod
    def config(
        cls, 
        tags: tuple[str, ...] = ("--config",),
        default: str | Callable[[], str] = "config.json",
    ) -> Option:
        return option(
            *tags,
            default=default,
            help="Path to the config file (JSON).",
            type=Path(resolve_path=True, dir_okay=False),
        )

    @classmethod
    def linelist(
        cls, 
        tags: tuple[str, ...] = ("--linelist",),
        default: str | Callable[[], str] = "linelist.csv",
    ) -> Option:
        return option(
            *tags,
            default=default,
            help="Path to the linelist file (CSV).",
            type=Path(resolve_path=True, dir_okay=False),
        )

    @classmethod
    def lookup(
        cls, 
        tags: tuple[str, ...] = ("--lookup",),
        default: str | Callable[[], str] = "lookup.csv",
    ) -> Option:
        return option(
            *tags,
            default=default,
            help="Path to the lookup file (CSV).",
            type=Path(resolve_path=True, dir_okay=False),
        )
    
    @classmethod
    def workspace(
        cls, 
        tags: tuple[str, ...] = ("--workspace",),
        default: str | Callable[[], str] = "workspace",
    ) -> Option:
        return option(
            *tags,
            default=default,
            help="Path to the workspace directory.",
            type=Path(resolve_path=True, file_okay=False),
        )

    @classmethod
    def output_path(
        cls, 
        tags: tuple[str, ...] = ("--output-path",),
        default: str | Callable[[], str] = "output",
    ) -> Option:
        return option(
            *tags,
            default=default,
            help="Path to the output directory.",
            type=Path(resolve_path=True),
        )

    @classmethod
    def start(cls, tags: tuple[str, ...] = ("--start",)) -> Option:
        return option(
            *tags,
            default=0,
            help="Start the process at the specified index.",
            type=int,
        )

    @classmethod
    def stop(cls, tags: tuple[str, ...] = ("--stop",)) -> Option:
        return option(
            *tags,
            help="Stop the process at the specified index.",
            default=-1,
            type=int,
        )

class PlotOptions(BaseParameters):
    @classmethod
    def styles(cls, tags: tuple[str, ...] = ("--styles",)) -> Option:
        return option(
            *tags,
            default=("science", "ieee"),
            help="List of plot styles.",
            type=tuple[str, ...],
        )

    @classmethod
    def dpi(cls, tags: tuple[str, ...] = ("--dpi",)) -> Option:
        return option(
            *tags,
            default=100,
            help="DPI used for plotting.",
            type=int,
        )

    @classmethod
    def name(cls, tags: tuple[str, ...] = ("--name",), default="plot.png") -> Option:
        return option(
            *tags,
            default=default,
            help="Filename for the plot (format is inferred from suffix).",
            type=str,
        )

class BootstrapOptions(BaseParameters):
    @classmethod
    def model_types(
        cls,
        tags: tuple[str, ...] = ("-M", "--mtypes",),
        default: tuple[str, ...] = (),
    ) -> Option:
        return option(
            *tags,
            default=default,
            multiple=True,
            help="Model types to include. Default: ().",
        )

    @classmethod
    def data_types(
        cls,
        tags: tuple[str, ...] = ("-D", "--dtypes",),
        default: tuple[str, ...] = (),
    ) -> Option:
        return option(
            *tags,
            default=default,
            multiple=True,
            help="Data types to include. Default: ().",
        )

class AnalysisOptions(BaseParameters):
    @classmethod
    def pattern(
        cls,
        tags: tuple[str, ...] = ("--pattern",),
        default: tuple[str, ...] = (),
    ) -> Option:
        return option(
            *tags,
            default=default,
            help="Target regex pattern for analysis.",
            type=str,
            multiple=True,
        )

    @classmethod
    def line(
        cls,
        tags: tuple[str, ...] = ("--line",),
        default: tuple[str, ...] = (),
    ) -> Option:
        return option(
            *tags,
            default=default,
            help="Target line (pure) name used for analysis.",
            type=str,
            multiple=True,
        )

    @classmethod
    def wave(
        cls,
        tags: tuple[str, ...] = ("--wave",),
        default: tuple[float, ...] = (),
    ) -> Option:
        return option(
            *tags,
            default=default,
            help="Target wave used for analysis.",
            type=float,
            multiple=True,
        )

    @classmethod
    def v_int(
        cls,
        tags: tuple[str, ...] = ("--v-int",),
        default: float = -1,
    ) -> Option:
        return option(
            *tags,
            default=default,
            help="Velocity interval (km/s) used when masking spectral "\
                "regions. If set to -1, the default value from the config "\
                "file is used. If set to 0, '--ipv-int' or '--dx-int' is used "\
                "instead.",
            type=float,
        )

    @classmethod
    def ipv_int(
        cls,
        tags: tuple[str, ...] = ("--ipv-int",),
        default: float = -1,
    ) -> Option:
        return option(
            *tags,
            default=default,
            help="Inter-percentile interval (%) used when masking spectral "\
                "regions. If set to -1, the default value from the config "\
                "file is used. If set to 0, '--dx-int' is used "\
                "instead.",
            type=float,
        )

    @classmethod
    def dx_int(
        cls,
        tags: tuple[str, ...] = ("--dx-int",),
        default: float = -1,
    ) -> Option:
        return option(
            *tags,
            default=default,
            help="Wavelength half-width (angstrom) used when masking spectral "\
                "regions. If set to -1, the default value from the config "\
                "file is used. If this and all other intervals are set to 0, " \
                "an error is raised.",
            type=float,
        )


class MeasureOptions(BaseParameters):
    @classmethod
    def bg(
        cls,
        tags: tuple[str, ...] = ("--bg",),
        default: tuple[str, ...] = (),
    ) -> Option:
        return option(
            *tags,
            default=default,
            help="Background flux components to subtract.",
            type=str,
            multiple=True,
        )

    @classmethod
    def unit(
        cls,
        tags: tuple[str, ...] = ("--unit",),
        *,
        default: str = "",
    ) -> Option:
        return option(
            *tags,
            default=default,
            help="Unit to convert measurement to.",
            type=str,
        )