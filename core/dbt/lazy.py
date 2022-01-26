# necessary for annotating constructors
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, cast, Generic, Optional, TypeVar


T = TypeVar('T')


# A data type for representing lazily evaluated values.
#
# usage:
# x = Lazy.defer(lambda: expensive_fn())
# y = x.force()
#
# inspired by the purescript data type
# https://pursuit.purescript.org/packages/purescript-lazy/5.0.0/docs/Data.Lazy
@dataclass
class Lazy(Generic[T]):
    _f: Callable[[], T]
    memo: Optional[T] = None

    # constructor for lazy values
    @classmethod
    def defer(cls, f: Callable[[], T]) -> Lazy[T]:
        return Lazy(f)

    # workaround for open mypy issue:
    # https://github.com/python/mypy/issues/6910
    def _typed_eval_f(self) -> T:
        return cast(Callable[[], T], getattr(self, "_f"))()

    # evaluates the function if the value has not been memoized already
    def force(self) -> T:
        if self.memo is None:
            self.memo = self._typed_eval_f()
        return self.memo
