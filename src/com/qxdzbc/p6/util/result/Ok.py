from typing import TypeVar, Generic

from com.qxdzbc.p6.util.result.Result import Result

T = TypeVar("T")

class Ok(Result[T,None],Generic[T]):

    def __init__(self, value):
        self.__value = value

    @property
    def err(self)->None:
        return None

    @property
    def value(self)->T:
        return self.__value

    def isOk(self):
        return True

    def isErr(self):
        return False