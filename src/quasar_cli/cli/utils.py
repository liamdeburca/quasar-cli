import pickle
from collections.abc import Callable
from pathlib import Path
from typing import TypeVar

F = TypeVar("F", bound=Callable)

def chain_decorators(*decorators) -> Callable[[F], F]:
    def wrapper(func: F) -> F:
        for decorator in reversed(decorators):
            func = decorator(func)
        return func
    return wrapper

class BaseParameters:
    @classmethod
    def chain(cls, *decorator_names) -> Callable[[F], F]:
        decorators = tuple(
            getattr(cls, name)()
            for name in decorator_names
        )
        return chain_decorators(*decorators)

def _get_context_path() -> Path:
    return Path.cwd() / ".cache/context.pkl"

def _load_context[C](cls: type[C]) -> C:
    """Load the context object from disk if it exists."""
    context_path = _get_context_path()
    try:
        with open(context_path, "rb") as f:
            ctx = pickle.load(f)
        return ctx
    except Exception:
        return cls()

def _save_context(ctx_obj: object) -> None:
    """Save the .obj attribute of a click.Context instance to disk."""
    context_path = _get_context_path()
    context_path.parent.mkdir(parents=True, exist_ok=True)
    with open(context_path, "wb") as f:
        pickle.dump(ctx_obj, f)

def _clear_context() -> None:
    """Clear the saved context from disk if it exists."""
    context_path = _get_context_path()
    context_path.unlink(missing_ok=True)