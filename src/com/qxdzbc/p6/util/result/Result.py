from typing import TypeVar, Generic

from com.qxdzbc.p6.util.report.error.ErrorReport import ErrorReport

V = TypeVar("V")
E = TypeVar("E")
M = TypeVar("M")


class Result(Generic[V, E]):

    @property
    def err(self) -> E:
        raise NotImplementedError()

    @property
    def value(self) -> V:
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

    def getOrRaise(self) -> V:
        """
        :return the enclosed value if this is an "Ok". If it is an "Err", raise it as an exception.
        """
        if self.isOk():
            return self.value
        else:
            if isinstance(self.err,ErrorReport):
                raise self.err.toException()
            elif isinstance(self.err, BaseException):
                raise self.err
            else:
                raise Exception(self.err)

    def getOrNone(self) -> V | None:
        if self.isOk():
            return self.value
        else:
            return None
    def raiseIfErr(self):
        if self.isErr():
            raise self.err
