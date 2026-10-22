from click import Option, option

from .utils import BaseParameters


class Flags(BaseParameters):
    @classmethod
    def verbose(cls) -> Option:
        return option(
            "-v", "--verbose",
            is_flag=True,
            help="Enable verbose output",
        )

    @classmethod
    def force(cls) -> Option:
        return option(
            "-f", "--force",
            is_flag=True,
            help="Enable force mode",
        )
    
    @classmethod
    def progress(cls) -> Option:
        return option(
            "-p", "--progress",
            is_flag=True,
            help="Enable progress bar",
        )

    @classmethod
    def fail_fast(cls) -> Option:
        return option(
            "-x", "--fail-fast",
            is_flag=True,
            help="Stop execution on the first error and raise it.",
        )

    @classmethod
    def clear_existing(cls) -> Option:
        return option(
            "--clear-existing",
            is_flag=True,
            help="Clear an output directory before running future processes.",
        )

    @classmethod
    def host_first(cls) -> Option:
        return option(
            "--host-first",
            is_flag=True,
            help="Fit the host galaxy contribution prior to the power law continuum.",
        )

class PlotFlags(BaseParameters):
    @classmethod
    def residual(cls) -> Option:
        return option(
            "--residual",
            is_flag=True,
            help="If set, the residuals are plotted rather than the data-model differences.",
        )

class MeasureFlags(BaseParameters):
    @classmethod
    def excess(cls) -> Option:
        return option(
            "--excess",
            is_flag=True,
            help="If set, measure the excess kurtosis.",
        )

    @classmethod
    def from_model(cls) -> Option:
        return option(
            "--from-model",
            is_flag=True,
            help="Measurements are based on model, not spectral, samples.",
        )