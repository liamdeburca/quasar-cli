import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter

_import_structure: dict[str, list[str]] = {
    "context": ["_Ctx", "_describe_context"],
    "lazy_dicts": [
        "LazyDict",
        "LazySpectrumDict",
        "LazyErrorResultDict",
        "LazyAnalyserDict",
        "LazyResultsDict"
    ]
}

if TYPE_CHECKING:
    from .context import _Ctx, _describe_context  # noqa: F401
    from .lazy_dicts import (  # noqa: F401
        LazyAnalyserDict,
        LazyDict,
        LazyErrorResultDict,
        LazyResultsDict,
        LazySpectrumDict,
    )
else:
    sys.modules[__name__] = LazyImporter(
        __name__,
        __file__,
        _import_structure,
    )