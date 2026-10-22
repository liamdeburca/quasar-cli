from abc import ABC, abstractmethod
from collections.abc import Callable, Hashable
from pathlib import Path
from typing import Any, TypeVar

from quasar_decrypt import Spectrum
from quasar_errors.analysis import Analyser
from quasar_errors.analysis.measure_result import FrozenMeasureResult
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
        if key not in self._subdir_map:
            raise KeyError(f"SubDir does not exist for {key=}")
        return self._subdir_map[key]

    def _context_helper(self, key: str, check_exists: bool = False) -> Path:
        path = self._subdir_helper(key) / ".context"
        if check_exists and not path.is_dir():
            raise KeyError(f"Context directory does not exist for {key=}")
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
            key = key.out_dir.stem

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
        path = self._subdir_helper(key) / "spectrum"
        if check_exists and not path.is_dir():
            raise KeyError(f"Spectrum directory does not exist for {key=}")
        return path
    
    def _loader(self, key: str) -> Spectrum:
        from quasar_decrypt.io import load_spectrum
        path = self._get_path(key, check_exists=True)
        return load_spectrum(path, self._config) 


    def _saver(self, key: str, value: Spectrum) -> None:
        from quasar_decrypt.io import dump_spectrum
        path = self._get_path(key)
        dump_spectrum(path, value, force=True)


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
        path = self._context_helper(key, check_exists=check_exists) / "error_result"
        if check_exists and not path.is_dir():
            raise KeyError(f"ErrorResult directory does not exist for {key=}")
        return path
    
    def _loader(self, key: str) -> ErrorResult:
        from quasar_errors.io.hdf5.error_result import load_error_result
        path = self._get_path(key, check_exists=True)
        return load_error_result(path, self._config)


    def _saver(self, key: str, value: ErrorResult) -> None:
        from quasar_errors.io.hdf5.error_result import dump_error_result
        path = self._get_path(key)
        dump_error_result(path, value, self._config, force=True)


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
        path = self._context_helper(key, check_exists=check_exists) / "analyser"
        if check_exists and not path.is_dir():
            raise KeyError(f"Analyser directory does not exist for {key=}")
        return path

    def _loader(self, key: str) -> Analyser:
        from quasar_errors.io.hdf5.analyser import load_analyser
        path = self._get_path(key, check_exists=True)
        return load_analyser(path, self._config)


    def _saver(self, key: str, value: Analyser) -> None:
        from quasar_errors.io.hdf5.analyser import dump_analyser
        path = self._get_path(key)
        dump_analyser(path, value, force=True)


class LazyResultsDict(LazyDict[str, dict[str, FrozenMeasureResult]]):
    """
    LazyDictionary for FrozenMeasureResult objects. 

    For a given `key`, the corresponding FrozenMeasureResult dictionary is loaded from disk 
    assuming the following directory structure exists:

    ```
    output_dir/
              <key>/
                   .context/
                           results.json
    ```
    """
    def _get_path(self, key: str, check_exists: bool = False) -> Path:
        path = self._context_helper(key, check_exists=check_exists) / "results.json"
        if check_exists and not path.is_file():
            raise KeyError(f"Results file does not exist for {key=}")
        return path 
    
    def _loader(self, key: str) -> dict[str, FrozenMeasureResult]:
        from quasar_errors.io.serialization.measure_result import (
            load_measure_results,
        )
        path = self._get_path(key, check_exists=True)
        return load_measure_results(path)

    def _saver(self, key: str, value: dict[str, FrozenMeasureResult]) -> None:
        from quasar_errors.io.serialization.measure_result import (
            dump_measure_results,
        )
        path = self._get_path(key)
        dump_measure_results(path, value)