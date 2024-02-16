# This file is more self-sustained and shouldn't use things from other higher-level modules.
from __future__ import annotations

from collections.abc import Iterable
from typing import Callable, TypeVar, overload

_T = TypeVar("_T")
_U = TypeVar("_U")


@overload
def first_true(
    items: Iterable[_T],
    default: _U,
    pred: Callable[[_T], bool] | None = None,
) -> _T | _U: ...


@overload
def first_true(
    items: Iterable[_T],
    *,
    pred: Callable[[_T], bool] | None = None,
) -> _T | None: ...


def first_true(
    items: Iterable[_T],
    default: _U | None = None,
    pred: Callable[[_T], bool] | None = None,
) -> _T | _U | None:
    """
    Gets the first item which satisfies the `pred`. Otherwise, `default`.
    If `pred` is not given or `None`, the first truthy item will be returned.
    """
    return next(filter(pred, items), default)
