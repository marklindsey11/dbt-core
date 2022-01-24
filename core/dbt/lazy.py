# necessary for annotating constructors
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, cast, Generic, Optional, TypeVar


T = TypeVar('T')


# A data type for representing lazily evaluated values. Evaluation is explicilty
# called with either `value` for access to memoization, or `force` to skip
# memoization.
#
# inspired by the purescript data type with
# additional considerations for impurity
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

    # gets the value from memoization or by evaluating the function.
    # good when the deferred function is pure.
    def value(self) -> T:
        if self.memo:
            return self.memo
        else:
            self.memo = self._typed_eval_f()
            return self.memo

    # forces evaluation skipping the memoization.
    # necessary for when the deferred funciton is stateful or impure.
    def force(self) -> T:
        return self._typed_eval_f()
