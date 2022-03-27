from bicp_document_structure.util.ToRepStr import ToRepStr

from bicp_document_structure.util.report.error.ErrorHeader import ErrorHeader

WSErr = "WSErr"


class WorksheetErrors:
    class IllegalName:
        header = ErrorHeader(f"{WSErr}1", "Illegal worksheet name")
        class Data(ToRepStr):
            def __init__(self, name: str | None):
                self.name: str | None = name

            def repStr(self) -> str:
                if self.name is None:
                    return "Sheet can't be null"
                else:
                    return "Sheet name must not be empty"
