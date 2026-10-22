from abc import ABC, abstractmethod
from dataclasses import field

from pydantic.dataclasses import dataclass
from quasar_decrypt import Spectrum
from quasar_utils.linelist import LineList
from quasar_utils.pipeline import OutputDir, SubDir
from quasar_utils.setup import Info

from ..utils import _map


@dataclass
class BasePipeline(ABC):
    config: Info = field(kw_only=True)
    linelist: LineList = field(kw_only=True)
    output_dir: OutputDir = field(kw_only=True)
    
    start: int = field(kw_only=True)
    stop: int = field(kw_only=True)

    host_first: bool = field(kw_only=True)
    force: bool = field(kw_only=True)
    progress: bool = field(kw_only=True)
    fail_fast: bool = field(kw_only=True)

    @abstractmethod
    def _load_spectrum(self, subdir: SubDir) -> Spectrum:
        ...

    def _fit_spectrum(self, spectrum: Spectrum) -> None:
        model_types = set()

        ### FIT CONTINUUM COMPONENTS
    
        if self.host_first:
            if (self.config.host.fit) \
                and (spectrum.x[-1] > self.config.host.x_min):
                spectrum.fitHost()
                model_types.add("hg")

            if self.config.continuum.fit:
                spectrum.fitContinuum()
                model_types.add("pl")

            if self.config.balmer.fit \
                and (spectrum.x[-1] > self.config.balmer.x_min):
                spectrum.fitBalmer()
                model_types.add("ba")

            if self.config.iron.fit:
                spectrum.fitIron()
                model_types.add("fe")

        else:
            if self.config.continuum.fit:
                spectrum.fitContinuum()
                model_types.add("pl")

            if self.config.balmer.fit \
                and (spectrum.x[-1] > self.config.balmer.x_min):
                spectrum.fitBalmer()
                model_types.add("ba")

            if self.config.iron.fit:
                spectrum.fitIron()
                model_types.add("fe")

            if (self.config.host.fit) \
                and (spectrum.x[-1] > self.config.host.x_min):
                spectrum.fitHost()
                model_types.add("hg")

        # Combined fit on all spectral windows
        spectrum.finaliseFit(
            model_types=model_types, 
            data_types=model_types,
        )

        ### FIT EMISSION LINES

        spectrum.fitLines(self.linelist)

        # Final fit on the entire spectrum
        spectrum.finaliseFit()

    def run(self) -> tuple[dict[str, Spectrum], None | list[str]]:
        msgs: list[str] = ["Failed to load/fit spectra:"]
        spectra: dict[str, Spectrum] = {}

        def func(i: int, subdir: SubDir) -> None:
            key = subdir.in_file.stem
            with subdir:
                try:
                    spectrum = self._load_spectrum(subdir)
                    spectra[key] = spectrum
                except Exception as exc:
                    msgs.append(
                        f"> [LOADING] {key}: {i=}, {exc=}"
                    )
                    if self.fail_fast:
                        raise
                    return

                try:
                    self._fit_spectrum(spectrum)
                except Exception as exc:
                    msgs.append(
                        f"> [FITTING] {key}: {i=}, {exc=}"
                    )
                    if self.fail_fast:
                        raise

        def desc_func(subdir: SubDir) -> str:
            return subdir.in_file.stem

        _map(
            func, self.output_dir,
            start=self.start, 
            stop=self.stop, 
            progress=self.progress, 
            desc_func=desc_func,
        )

        spectra = dict(filter(
            lambda item: item[1] is not None, 
            spectra.items(),
        ))
        return spectra, msgs
