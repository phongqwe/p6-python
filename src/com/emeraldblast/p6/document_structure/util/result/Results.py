from typing import Any

from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.emeraldblast.p6.document_structure.util.result.Result import Result


class Results:
    @staticmethod
    def extractOrRaise(result:Result[Any,ErrorReport]):
        """extract the value or raise the err as an exception"""
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