from abc import ABC
from typing import Generic, TypeVar

A = TypeVar("A")
B = TypeVar("B")


class TwoWayRef(Generic[A, B], ABC):
    def cut(self):
        raise NotImplementedError()

    @property
    def a(self) -> A | None:
        raise NotImplementedError()

    @property
    def b(self) -> B | None:
        raise NotImplementedError()

    def isValid(self):
        return self.a is not None and self.b is not None
