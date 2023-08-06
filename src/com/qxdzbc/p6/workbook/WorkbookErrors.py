from typing import Union

from com.qxdzbc.p6.util.ToException import ToException
from com.qxdzbc.p6.util.ToRepStr import ToRepStr
from com.qxdzbc.p6.util.report.error.ErrorHeader import ErrorHeader
from com.qxdzbc.p6.util.report.error.ErrorReport import ErrorReport

WBErr = "BE_WorkbookErrors_"


class WorkbookErrors:
    class WorksheetAlreadyExistReport(ErrorReport):
        header = ErrorHeader(f"{WBErr}1", "worksheet already exist")

        class Data(ToRepStr, ToException):
            def __init__(self, nameOrIndex: Union[str, int]):
                self.name = None
                self.index = None
                if isinstance(nameOrIndex, str):
                    self.name = nameOrIndex
                if isinstance(nameOrIndex, int):
                    self.index = nameOrIndex

            def repStr(self) -> str:
                if self.name is not None:
                    return f"Can't create worksheet \"{self.name}\". It already exists"
                else:
                    return "Can't create new worksheet"

            def toException(self) -> Exception:
                return Exception(
                    f"{WorkbookErrors.WorksheetAlreadyExistReport.header.errorCode}:{self.repStr()}"
                )
        def __init__(self,nameOrIndex: Union[str, int]):
            super().__init__(
                WorkbookErrors.WorksheetAlreadyExistReport.header,
                WorkbookErrors.WorksheetAlreadyExistReport.Data(nameOrIndex)
            )

    class WorksheetNotExistReport(ErrorReport):
        header = ErrorHeader(f"{WBErr}2", "worksheet not exist")

        class Data(ToRepStr, ToException):
            def __init__(self, nameOrIndex: Union[str, int]):
                self.name = None
                self.index = None
                if isinstance(nameOrIndex, str):
                    self.name = nameOrIndex
                if isinstance(nameOrIndex, int):
                    self.index = nameOrIndex

            def __str__(self):
                return self.repStr()

            def repStr(self) -> str:
                if self.name:
                    return f"Worksheet \"{self.name}\" does not exist"
                if self.index:
                    return f"Worksheet at index \"{self.index}\" does not exist"
                return "No Worksheet with blank name"

            def toException(self) -> Exception:
                return ValueError(
                    f"{WorkbookErrors.WorksheetAlreadyExistReport.header.errorCode}:{self.repStr()}"
                )
        def __init__(self,nameOrIndex: Union[str, int]):
            super().__init__(
                WorkbookErrors.WorksheetNotExistReport.header,
                WorkbookErrors.WorksheetNotExistReport.Data(nameOrIndex)
            )
        @staticmethod
        def report(detail:str=None):
            if detail:
                return ErrorReport(
                    header = WorkbookErrors.WorksheetNotExistReport.header.setDescription(detail),
                )
            else:
                return ErrorReport(
                    header = WorkbookErrors.WorksheetNotExistReport.header,
                )