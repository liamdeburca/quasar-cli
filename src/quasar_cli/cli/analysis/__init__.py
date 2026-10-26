import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter

_import_structure: dict[str, list[str]] = {
    "analysis": [
        "_analysis_isolate",
        "analysis_exit",
    ],
    "measure": [
        "_cen",
        "_strength",
        "_fwhm_vel",
        "_ew",
        "_lum",
    ]
}

if TYPE_CHECKING:
    from .analysis import (  # noqa: F401
        _analysis_isolate,
        analysis_exit,
    )
    from .measure import (  # noqa: F401
        _cen,
        _ew,
        _fwhm_vel,
        _lum,
        _strength,
    )
else:
    sys.modules[__name__] = LazyImporter(
        __name__,
        __file__,
        _import_structure,
    )
