from typing import ClassVar

from click import Argument, Path, argument

from .utils import BaseParameters


class Arguments(BaseParameters):
    @classmethod
    def fname(cls, nargs: int = 1) -> Argument:
        if nargs == -1:
            _help = "Any number of filenames."
        elif nargs == 1:
            _help = "File name."
        else:
            _help = f"{nargs} filenames."

        return argument(
            "fname",
            help=_help,
            nargs=nargs,
            type=str,
            required=True
        )

class PathArguments(BaseParameters):
    exists: ClassVar[bool] = True

    @classmethod
    def config(cls) -> Argument:
        return argument(
            "config",
            default="config.json",
            type=Path(exists=cls.exists, dir_okay=False),
            help=f"Path to a config file (exists={cls.exists})",
        )

    @classmethod
    def linelist(cls) -> Argument:
        return argument(
            "linelist",
            default="linelist.csv",
            type=Path(exists=cls.exists, dir_okay=False),
            help=f"Path to a linelist file (exists={cls.exists})",
        )

    @classmethod
    def lookup(cls) -> Argument:
        return argument(
            "lookup",
            default="lookup.csv",
            type=Path(exists=cls.exists, dir_okay=False),
            help=f"Path to a lookup file (exists={cls.exists})",
        )

    @classmethod
    def workspace(cls) -> Argument:
        return argument(
            "workspace",
            default="workspace",
            type=Path(exists=cls.exists, file_okay=False),
            help=f"Path to a workspace directory (exists={cls.exists})",
        )

    @classmethod
    def output(cls) -> Argument:
        return argument(
            "output",
            default="output",
            type=Path(exists=cls.exists, file_okay=False),
            help=f"Path to an output directory (exists={cls.exists})",
        )

    @classmethod
    def input_path(cls) -> Argument:
        return argument(
            "input-path",
            type=Path(exists=cls.exists),
            help=f"Path to an input file/directory (exists={cls.exists})",
        )

class AnyPathArguments(PathArguments):
    exists: ClassVar[bool] = False

class MeasureArguments(BaseParameters):
    @classmethod
    def name(cls) -> Argument:
        return argument(
            "name",
            type=str,
            help="Name for the measurement.",
            required=True
        )
        
    @classmethod
    def lb(cls) -> Argument:
        return argument(
            "lb",
            type=float,
            help="Lower bound for the measurement.",
            required=True
        )

    @classmethod
    def ub(cls) -> Argument:
        return argument(
            "ub",
            type=float,
            help="Upper bound for the measurement.",
            required=True
        )

    @classmethod
    def q(cls) -> Argument:
        return argument(
            "q",
            type=float,
            help="Quantile for the measurement.",
            required=True
        )

    @classmethod
    def p(cls) -> Argument:
        return argument(
            "p",
            type=float,
            help="Percentile for the measurement.",
            required=True
        )

    @classmethod
    def h(cls) -> Argument:
        return argument(
            "h",
            type=float,
            help="Height for the measurement.",
            required=True
        )