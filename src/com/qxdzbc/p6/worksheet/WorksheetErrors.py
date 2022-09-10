from typing import Optional

from com.qxdzbc.p6.util import ToRepStr
from com.qxdzbc.p6.util.report.error.ErrorHeader import ErrorHeader
from com.qxdzbc.p6.util.report.error.ErrorReport import ErrorReport

WSErr = "BE_WorksheetErrors_"


class WorksheetErrors:
    class IllegalNameReport(ErrorReport):
        header = ErrorHeader(f"{WSErr}1", "Illegal worksheet name")

        class Data(ToRepStr):
            def __init__(self, name: Optional[str]):
                self.name: Optional[str] = name

            def repStr(self) -> str:
                if self.name is None:
                    return "Sheet can't be null"
                else:
                    return "Sheet name must not be empty"

        def __init__(self, name: Optional[str]):
            super().__init__(
                WorksheetErrors.IllegalNameReport.header,
                WorksheetErrors.IllegalNameReport.Data(name))
