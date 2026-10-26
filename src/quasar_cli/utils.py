from collections.abc import Callable, Iterable
from pathlib import Path
from typing import ClassVar

import click
from quasar_utils.pipeline import OutputDir, SubDir

_this_file: Path = Path(__file__).resolve()

class DefaultPaths:
    config: ClassVar[Path] = _this_file.parent / "data/config.json"
    linelist: ClassVar[Path] = _this_file.parent / "data/linelist.csv"
    lookup: ClassVar[Path] = _this_file.parent / "data/lookup.csv"

def _get_output_dir(output_path: str | Path):

    output_path: Path = Path(output_path).resolve()
    if output_path.stem.endswith("_out") and output_path.is_dir():
        output_path = output_path.parent
        
    return OutputDir.resume(output_path)

def _get_subdirs(output_path: str | Path) -> list[SubDir]:
    output_path: Path = Path(output_path).resolve()
    if output_path.stem.endswith("_out") and output_path.is_dir():
        filter_func = lambda s: s.out_dir.stem == output_path.stem
    else:
        filter_func = lambda s: True

    output_dir = _get_output_dir(output_path)
    return list(filter(filter_func, output_dir))

def _get_subdir_paths(output_path: str | Path) -> list[Path]:
    output_path: Path = Path(output_path).resolve()
    if output_path.stem.endswith("_out") and output_path.is_dir():
        # Specific spectrum has been selected
        return [output_path]
    return sorted(
        [
            p
            for p in output_path.iterdir()
            if p.stem.endswith("_out") and p.is_dir()
        ],
        key=lambda p: p.stem,
    )

def _get_spectrum(subdir: SubDir, verbose: bool):
    from quasar_decrypt import Spectrum

    spectrum_path = subdir.out_dir / "spectrum.pkl"
    if not spectrum_path.exists():
        if verbose: 
            click.echo(f"Spectrum file does not exist at: {spectrum_path!s}")
        raise FileNotFoundError(spectrum_path)
    
    try:
        spectrum = Spectrum.load(spectrum_path)
        if verbose:
            click.echo(f"Loaded spectrum: {spectrum.title}")
        return spectrum
    except Exception as exc:
        msg = f"Failed to load spectrum at: {spectrum_path!s}!"
        if verbose:
            click.echo(msg)
        raise ValueError(msg) from exc


def _map[P, R](
    func: Callable[[int, P], R], 
    iterable: Iterable[P],
    *,
    start: int,
    stop: int,
    progress: bool,
    desc_func: Callable[[P], str] | None = None,
    **kwargs,
) -> list[R]:
    from tqdm import tqdm

    kwargs["disable"] = not progress
    loop = tqdm(iterable, **kwargs)
    out: list[R] = []

    for i, p in enumerate(loop):
        if desc_func is not None:
            loop.set_description(desc_func(p))

        if i < start or (stop >= 0 and i >= stop):
            continue

        out.append(func(i, p))

    return out
