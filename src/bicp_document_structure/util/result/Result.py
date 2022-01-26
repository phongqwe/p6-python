from typing import TypeVar, Generic

T = TypeVar("T")
E = TypeVar("E")

class Result(Generic[T,E]):

    @property
    def err(self)->E:
        raise NotImplementedError()

    def value(self)->T:
        raise NotImplementedError()

    def isOk(self):
        return self.value is not None

    def isErr(self):
        return self.err is not None

