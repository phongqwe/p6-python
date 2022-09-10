from abc import ABC
from typing import Generic, TypeVar

A = TypeVar("A")
B = TypeVar("B")


class TwoWayRef(Generic[A, B], ABC):
    """
    The point of two-way ref is that one party can severe the relation without leave dangling reference and memory leak and shit.
    """
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
