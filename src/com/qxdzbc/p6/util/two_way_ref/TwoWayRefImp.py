from typing import TypeVar

from com.qxdzbc.p6.util.two_way_ref.TwoWayRef import TwoWayRef

A = TypeVar("A")
B = TypeVar("B")


class TwoWayRefImp(TwoWayRef[A, B]):
    def __init__(self, a: A, b: B):
        self._a = a
        self._b = b

    @property
    def a(self) -> A | None:
        return self._a

    @property
    def b(self) -> B | None:
        return self._b

    def cut(self):
        self._a = None
        self._b = None
