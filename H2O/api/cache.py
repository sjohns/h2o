from __future__ import annotations

from functools import lru_cache
from typing import Callable

_solver_fn: Callable[[list[str]], dict] | None = None


def configure_solver_cache(solver_fn: Callable[[list[str]], dict]) -> None:
    global _solver_fn
    _solver_fn = solver_fn
    _solve_cached_internal.cache_clear()


@lru_cache(maxsize=10000)
def _solve_cached_internal(key: tuple[str, ...]) -> dict:
    if _solver_fn is None:
        raise RuntimeError("Solver cache used before configuration")
    return _solver_fn(list(key))


def solve_cached(key: tuple[str, ...]) -> dict:
    return _solve_cached_internal(key)
