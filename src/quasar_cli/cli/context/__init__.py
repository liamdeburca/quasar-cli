import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter

_import_structure: dict[str, list[str]] = {
    "context": ["_Ctx"],
    "context_utils": ["_describe_context", "_validate_context"],
    "lazy_dicts": [
        "LazyDict",
        "LazySpectrumDict",
        "LazyErrorResultDict",
        "LazyAnalyserDict",
        "LazyResultsDict"
    ]
}

if TYPE_CHECKING:
    from .context import _Ctx  # noqa: F401
    from .context_utils import (  # noqa: F401
        _describe_context,
        _validate_context,
    )
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