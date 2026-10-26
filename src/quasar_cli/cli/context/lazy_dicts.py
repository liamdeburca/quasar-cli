from abc import ABC, abstractmethod
from collections.abc import Callable, Hashable
from pathlib import Path
from typing import Any, TypeVar

from quasar_decrypt import Spectrum
from quasar_errors.analysis import Analyser
from quasar_errors.analysis.measure_result import (
    FrozenMeasureResult,
    MeasureResult,
)
from quasar_errors.error_result import ErrorResult
from quasar_utils.pipeline import OutputDir, SubDir
from quasar_utils.setup import Info

K = TypeVar("K", bound=Hashable)
V = TypeVar("V", bound=Any)
D = TypeVar("D", bound=Callable[[K, V], None])
L = TypeVar("L", bound=Callable[[K], V])


class LazyDict(dict[K, V], ABC):
    """
    Abstract base class for a lazy-loading dictionary.
    """
    def __init__(self, output_dir: OutputDir, config: Info):
        self._output_dir: OutputDir = output_dir
        self._config: Info = config
        self._subdir_map: dict[str, Path] = {
            subdir.in_file.stem: subdir.out_dir
            for subdir in output_dir
        }
        super().__init__()

    def _subdir_helper(self, key: str) -> Path:
        """Get the subdirectory path corresponding to the given key."""
        if key not in self._subdir_map:
            raise KeyError(f"SubDir does not exist for {key=}")
        return self._subdir_map[key]

    def _context_helper(self, key: str, check_exists: bool = False) -> Path:
        """Get the context directory path corresponding to the given key.
        
        If `check_exists` is True, raise a KeyError if the directory does not 
        exist.
        """
        path = self._subdir_helper(key) / ".context"
        if check_exists and not path.is_dir():
            raise KeyError(
                f"Context directory does not exist for {key=}: {path=}"
            )
        return path

    @abstractmethod
    def _get_path(self, key: K, check_exists: bool = False) -> Path:
        pass

    @abstractmethod
    def _loader(self, key: K) -> V:
        pass

    @abstractmethod
    def _saver(self, key: K, value: V) -> None:
        pass

    def __getitem__(self, key: K | SubDir) -> V:
        if isinstance(key, SubDir):
            key = key.in_file.stem
        key = key.removesuffix("_out")

        if key not in self:
            super().__setitem__(key, self._loader(key))
        return super().__getitem__(key)

    def __delitem__(self, key: K) -> None:
        if key in self:
            self._saver(key, self[key])
            super().__delitem__(key)

    def clear(self) -> None:
        for key in list(self.keys()):
            self.__delitem__(key)


    def get_length(self, output_dir: OutputDir) -> int:
        return sum(
            self._get_path(subdir.in_file.stem).exists()
            for subdir in output_dir
        )


###


class LazySpectrumDict(LazyDict[str, Spectrum]):
    """
    LazyDictionary for Spectrum objects. 

    For a given `key`, the corresponding Spectrum object is loaded from disk 
    assuming the following directory structure exists:

    ```
    output_dir/
              <key>/
                   spectrum/
    ```
    """
    def _get_path(self, key: str, check_exists: bool = False) -> Path:
        """Get the path to the spectrum directory for the given key.
        
        Raises a KeyError if `check_exists` is True and the directory does not 
        exist.
        """
        path = self._subdir_helper(key) / "spectrum"
        if check_exists and not path.is_dir():
            raise KeyError(f"Spectrum directory does not exist for {key=}")
        return path
    
    def _loader(self, key: str) -> Spectrum:
        """Load the Spectrum object for the given key."""
        from quasar_io import load_spectrum
        path = self._get_path(key, check_exists=True)
        return load_spectrum(path, self._config) 


    def _saver(self, key: str, value: Spectrum) -> None:
        """Save the Spectrum object for the given key."""
        from quasar_io import dump_spectrum
        path = self._get_path(key)
        dump_spectrum(path, value, exist_ok=True)


class LazyErrorResultDict(LazyDict[str, ErrorResult]):
    """
    LazyDictionary for ErrorResult objects. 

    For a given `key`, the corresponding ErrorResult object is loaded from disk 
    assuming the following directory structure exists:

    ```
    output_dir/
              <key>/
                   .context/
                           error_result/
    ```
    """
    def _get_path(self, key: str, check_exists: bool = False) -> Path:
        """Get the path to the ErrorResult directory for the given key.
        
        Raises a KeyError if `check_exists` is True and the directory does not 
        exist.
        """
        path = self._context_helper(key, check_exists=check_exists) / "error_result"
        if check_exists and not path.is_dir():
            raise KeyError(
                f"ErrorResult directory does not exist for {key=}: {path=}"
            )
        return path
    
    def _loader(self, key: str) -> ErrorResult:
        """Load the ErrorResult object for the given key."""
        from quasar_io import load_error_result
        path = self._get_path(key, check_exists=True)
        return load_error_result(path, self._config)


    def _saver(self, key: str, value: ErrorResult) -> None:
        """Save the ErrorResult object for the given key."""
        from quasar_io import dump_error_result
        path = self._get_path(key)
        dump_error_result(path, value, self._config, exist_ok=True)


class LazyAnalyserDict(LazyDict[str, Analyser]):
    """
    LazyDictionary for Analyser objects. 

    For a given `key`, the corresponding Analyser object is loaded from disk 
    assuming the following directory structure exists:

    ```
    output_dir/
              <key>/
                   .context/
                           analyser/
    ```
    """
    def _get_path(self, key: str, check_exists: bool = False) -> Path:
        """Get the path to the Analyser directory for the given key.
        
        Raises a KeyError if `check_exists` is True and the directory does not 
        exist.
        """
        path = self._context_helper(key, check_exists=check_exists) / "analyser"
        if check_exists and not path.is_dir():
            raise KeyError(
                f"Analyser directory does not exist for {key=}: {path=}"
            )
        return path

    def _loader(self, key: str) -> Analyser:
        """Load the Analyser object for the given key."""
        from quasar_io import load_analyser
        path = self._get_path(key, check_exists=True)
        return load_analyser(path, self._config)


    def _saver(self, key: str, value: Analyser) -> None:
        """Save the Analyser object for the given key."""
        from quasar_io import dump_analyser
        path = self._get_path(key)
        dump_analyser(path, value, self._config, exist_ok=True)


class LazyResultsDict(
    LazyDict[str, dict[str, MeasureResult | FrozenMeasureResult]]
):
    """
    LazyDictionary for MeasureResult and FrozenMeasureResult objects.

    For a given `key`, the corresponding MeasureResult and FrozenMeasureResult 
    dictionary is loaded from disk assuming the following directory structure 
    exists:
    ```
    output_dir/
              <key>/
                   .context/
                           results.json
    ```
    """
    def _get_path(self, key: str, check_exists: bool = False) -> Path:
        """
        Raises a KeyError if `check_exists` is True and the file does not exist.
        """
        path = self._context_helper(key, check_exists=check_exists) / "measure_result_dict"
        if check_exists and not path.is_dir():
            raise KeyError(
                f"Results file does not exist for {key=}: {path=}"
            )
        return path 
    
    def _loader(
        self, 
        key: str,
    ) -> dict[str, MeasureResult | FrozenMeasureResult]:
        """Load the (Frozen)MeasureResult dictionary for the given key."""
        from quasar_io import load_measure_result_dict
        path = self._get_path(key, check_exists=True)
        return load_measure_result_dict(path)

    def _saver(
        self, 
        key: str, 
        value: dict[str, MeasureResult | FrozenMeasureResult],
    ) -> None:
        """Save the (Frozen)MeasureResult dictionary for the given key."""
        from quasar_io import dump_measure_result_dict
        path = self._get_path(key)
        dump_measure_result_dict(path, value, exist_ok=True)