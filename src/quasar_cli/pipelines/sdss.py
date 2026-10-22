from pydantic.dataclasses import dataclass
from quasar_decrypt import Spectrum
from quasar_utils.loading import SDSSLoader
from quasar_utils.pipeline import SubDir

from .base_pipeline import BasePipeline


@dataclass
class SDSSPipeline(BasePipeline):
    def _load_spectrum(self, subdir: SubDir) -> Spectrum:
        loader = SDSSLoader(
            subdir.in_file,
            info=self.config,
        )
        return Spectrum.create(**loader())