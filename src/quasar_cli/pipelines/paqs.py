from dataclasses import field

from pydantic.dataclasses import dataclass
from quasar_decrypt import Spectrum
from quasar_utils.loading import PAQSLoader
from quasar_utils.pipeline import SubDir

from .base_pipeline import BasePipeline


@dataclass
class PAQSPipeline(BasePipeline):
    redshifts: dict[str, float] = field(kw_only=True)
    ras: dict[str, float] = field(kw_only=True)
    decs: dict[str, float] = field(kw_only=True)

    def _load_spectrum(self, subdir: SubDir) -> Spectrum:
        uid = subdir.in_file.stem
        loader = PAQSLoader(
            subdir.in_file,
            info=self.config,
            z=self.redshifts[uid],
            ra=self.ras[uid],
            dec=self.decs[uid],
        )
        return Spectrum.create(**loader())