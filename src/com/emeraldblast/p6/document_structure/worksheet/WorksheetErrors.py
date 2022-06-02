from com.emeraldblast.p6.document_structure.util.ToRepStr import ToRepStr

from com.emeraldblast.p6.document_structure.util.report.error.ErrorHeader import ErrorHeader
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport

WSErr = "BE_WorksheetErrors_"


class WorksheetErrors:
    class IllegalNameReport(ErrorReport):
        header = ErrorHeader(f"{WSErr}1", "Illegal worksheet name")

        class Data(ToRepStr):
            def __init__(self, name: str | None):
                self.name: str | None = name

            def repStr(self) -> str:
                if self.name is None:
                    return "Sheet can't be null"
                else:
                    return "Sheet name must not be empty"

        def __init__(self, name: str | None):
            super().__init__(
                WorksheetErrors.IllegalNameReport.header,
                WorksheetErrors.IllegalNameReport.Data(name))
    @staticmethod
    def CantPasteFromNonDataFrameObj()-> ErrorReport:
        return ErrorReport(
            header = ErrorHeader(
                errorCode = f"{WSErr}2",
                errorDescription = "Can't paste from a non-DataFrame obj in clipboard"
            )
        )
