import pickle
from dataclasses import dataclass
from pathlib import Path
from shutil import rmtree

from quasar_utils.linelist import LineList
from quasar_utils.pipeline import InputDir, OutputDir
from quasar_utils.setup import Info

from .lazy_dicts import (
    LazyAnalyserDict,
    LazyDict,
    LazyErrorResultDict,
    LazyResultsDict,
    LazySpectrumDict,
)


@dataclass
class _Ctx:
    _path: Path | None = None

    _config: Info | None = None
    _linelist: LineList | None = None
    _input_dir: InputDir | None = None
    _output_dir: OutputDir | None = None

    _spectra: LazySpectrumDict | None = None
    _error_results: LazyErrorResultDict | None = None
    _analysers: LazyAnalyserDict | None = None
    _results: LazyResultsDict | None = None

    _has_changed: set[str] | None = None

    def __enter__(self):
        assert self._path is None
        self.open()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    @property
    def path(self) -> Path:
        assert self._path is not None
        self._path.mkdir(parents=True, exist_ok=True)
        return self._path

    def open(self) -> None:
        self._path = Path.cwd() / ".context"
        self._has_changed = set()

    def close(self) -> None:
        """Write cached values to disk."""
        del self.config
        del self.linelist
        del self.input_dir
        del self.output_dir

        del self.spectra
        del self.error_results
        del self.analysers
        del self.results
        
        self._path = None
        self._has_changed = None

    def __contains__(self, item: str) -> bool:
        """
        Check if the specified context item exists.
        """
        match item:
            case "config":
                return (self._path / "config.json").exists()
            case "linelist":
                return (self._path / "linelist.csv").exists()
            case "input_dir":
                return (self._path / "input_dir.pkl").exists()
            case "output_dir":
                return (self._path / "output_dir.pkl").exists()
            case "spectra":
                return (self.spectra is not None) \
                    and self.spectra.get_length(self._output_dir)
            case "error_results":
                return (self.error_results is not None) \
                    and self.error_results.get_length(self._output_dir)
            case "analysers":
                return (self.analysers is not None) \
                    and self.analysers.get_length(self._output_dir)
            case "results":
                return (self.results is not None) \
                    and self.results.get_length(self._output_dir)
        return False

    def remove(self, item: str) -> None:
        """
        Set the attribute to None and delete the associated file.
        """
        if item not in self:
            return

        if item in {"config", "linelist", "input_dir", "output_dir"}:
            p = self._path / {
                "config": "config.json",
                "linelist": "linelist.csv",
                "input_dir": "input_dir.pkl",
                "output_dir": "output_dir.pkl",
            }[item]
            setattr(self, f"_{item}", None)
            p.unlink(missing_ok=True)
        else:
            d: LazyDict = getattr(self, f"_{item}")
            for key in d:
                path = d._get_path(key)
                
                if path.is_file():
                    path.unlink()
                elif path.is_dir():
                    rmtree(path)

    ### CONFIG

    @property
    def config(self) -> Info:
        if self._config is not None:
            return self._config
        self._config = Info.from_json(self._path / "config.json")
        return self._config

    @config.setter
    def config(self, value: str | Path | Info) -> None:
        if isinstance(value, (str, Path)):
            value = Info.from_json(value)
        self._config = value
        self._has_changed.add("config")

    @config.deleter
    def config(self) -> None:
        if self._config is None or "config" not in self._has_changed:
            return

        self._config.to_json(self.path / "config.json")
        self._config = None
        self._has_changed.remove("config")

    ### LINELIST

    @property
    def linelist(self) -> LineList:
        if self._linelist is None:
            self._linelist = LineList.read_csv(
                path=self._path / "linelist.csv", 
                info=self.config,
            )
        return self._linelist

    @linelist.setter
    def linelist(self, value: str | Path | LineList) -> None:
        if isinstance(value, (str, Path)):
            value = LineList.read_csv(path=value, info=self.config)
        self._linelist = value
        self._has_changed.add("linelist")

    @linelist.deleter
    def linelist(self) -> None:
        if self._linelist is None or "linelist" not in self._has_changed:
            return

        self._linelist.to_csv(self.path / "linelist.csv")
        self._linelist = None
        self._has_changed.remove("linelist")

    ### INPUT DIR

    @property
    def input_dir(self) -> InputDir:
        if self._input_dir is not None:
            return self._input_dir
        with open(self._path / "input_dir.pkl", "rb") as f:
            self._input_dir = pickle.load(f)        
        return self._input_dir

    @input_dir.setter
    def input_dir(self, value: str | Path | InputDir) -> None:
        if isinstance(value, (str, Path)):
            p = Path(value)
            with open(p, "rb") as f:
                value = pickle.load(f)
        self._input_dir = value
        self._has_changed.add("input_dir")

    @input_dir.deleter
    def input_dir(self) -> None:
        if self._input_dir is None or "input_dir" not in self._has_changed:
            return
        with open(self._path / "input_dir.pkl", "wb") as f:
            pickle.dump(self._input_dir, f)
        self._input_dir = None
        self._has_changed.remove("input_dir")

    ### OUTPUT DIR

    @property
    def output_dir(self) -> OutputDir:
        if self._output_dir is not None:
            return self._output_dir
        with open(self._path / "output_dir.pkl", "rb") as f:
            self._output_dir = pickle.load(f)
        return self._output_dir

    @output_dir.setter
    def output_dir(self, value: str | Path | OutputDir) -> None:
        if isinstance(value, (str, Path)):
            p = Path(value)
            with open(p, "rb") as f:
                value = pickle.load(f)
        self._output_dir = value
        self._has_changed.add("output_dir")

    @output_dir.deleter
    def output_dir(self) -> None:
        if self._output_dir is None or "output_dir" not in self._has_changed:
            return
        with open(self._path / "output_dir.pkl", "wb") as f:
            pickle.dump(self._output_dir, f)
        self._output_dir = None
        self._has_changed.remove("output_dir")

    ###

    @property
    def spectra(self) -> LazySpectrumDict | None:
        if (self.output_dir is not None) and self._spectra is None:
            self._spectra = LazySpectrumDict(self.output_dir, self.config)
        return self._spectra

    @spectra.deleter
    def spectra(self) -> None:
        if self._spectra is not None:
            self._spectra.clear()
            self._spectra = None

    ###

    @property
    def error_results(self) -> LazyErrorResultDict:
        if (self.output_dir is not None) and self._error_results is None:
            self._error_results = LazyErrorResultDict(self.output_dir, self.config)
        return self._error_results

    @error_results.deleter
    def error_results(self) -> None:
        if self._error_results is not None:
            self._error_results.clear()
            self._error_results = None

    ###

    @property
    def analysers(self) -> LazyAnalyserDict | None:
        if (self.output_dir is not None) and self._analysers is None:
            self._analysers = LazyAnalyserDict(self.output_dir, self.config)
        return self._analysers


    @analysers.deleter
    def analysers(self) -> None:
        if self._analysers is not None:
            self._analysers.clear()
            self._analysers = None

    ###

    @property
    def results(self) -> LazyResultsDict | None:
        if (self.output_dir is not None) and self._results is None:
            self._results = LazyResultsDict(self.output_dir, self.config)
        return self._results

    @results.deleter
    def results(self) -> None:
        if self._results is not None:
            self._results.clear()
            self._results = None