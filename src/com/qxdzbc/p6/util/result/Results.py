from typing import Any

from com.qxdzbc.p6.util.report.error.ErrorReport import ErrorReport
from com.qxdzbc.p6.util.result.Result import Result


class Results:
    @staticmethod
    def extractOrRaise(result:Result[Any,ErrorReport]):
        """
        @deprecated: don't use this. use "getOrRaise" directly on Result objs
        extract the value or raise the err as an exception
        """
        if result.isOk():
            return result.value
        else:
            raise result.err.toException()

    @staticmethod
    def extractOrNone(result:Result[Any,ErrorReport]):
        if result.isOk():
            return result.value
        else:
            return None