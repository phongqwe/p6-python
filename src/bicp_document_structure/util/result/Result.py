from typing import TypeVar, Generic

T = TypeVar("T")
E = TypeVar("E")

class Result(Generic[T,E]):

    @property
    def err(self)->E:
        raise NotImplementedError()

    @property
    def value(self)->T:
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