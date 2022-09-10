from com.qxdzbc.p6.util.ToException import ToException
from com.qxdzbc.p6.util.ToRepStr import ToRepStr
from com.qxdzbc.p6.util.report.error.ErrorHeader import ErrorHeader
from com.qxdzbc.p6.util.report.error.ErrorReport import ErrorReport

CE = "BE_CommonErrors_"
class CommonErrors:


    class WrongTypeReport(ErrorReport):
        header = ErrorHeader(f"{CE}0", "Incorrect type")
        class Data(ToRepStr,ToException):
            def __init__(self,varName:str, correctType:str):
                self.varName = varName
                self.correctType = correctType

            def repStr(self) -> str:
                return f"\"{self.varName}\" must be {self.correctType}"

            def toException(self) -> Exception:
                return Exception(self.repStr())
        def __init__(self, varName:str,correctType:str):
            data =CommonErrors.WrongTypeReport.Data(varName,correctType)
            super().__init__(CommonErrors.WrongTypeReport.header, data)

    class ExceptionErrorReport(ErrorReport):
        """
        for reporting exception as ErrorReport
        """
        header = ErrorHeader(f"{CE}1", "Exception error")

        class Data(ToRepStr, ToException):
            def __init__(self, exception: Exception):
                self._e = exception

            def repStr(self) -> str:
                return f"Encounter exception: {self._e}"

            def toException(self) -> Exception:
                return self._e

        def __init__(self, exception: Exception):
            super().__init__(
                header = CommonErrors.ExceptionErrorReport.header,
                data = CommonErrors.ExceptionErrorReport.Data(exception)
            )
        @staticmethod
        def report(exception: Exception)->ErrorReport:
            return CommonErrors.ExceptionErrorReport(exception)

    CommonError = ErrorReport(
        header = ErrorHeader(f"{CE}3", "common error")
    )