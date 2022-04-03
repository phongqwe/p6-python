from abc import ABC
from typing import TypeVar, Generic

V = TypeVar("V")
E = TypeVar("E")

class Result(Generic[V, E]):

    @property
    def err(self)->E:
        raise NotImplementedError()

    @property
    def value(self)->V:
        raise NotImplementedError()

    def getEither(self):
        if self.isOk():
            return self.value
        else:
            return self.err

    def isOk(self):
        return self.value is not None

    def isErr(self):
        return self.err is not None