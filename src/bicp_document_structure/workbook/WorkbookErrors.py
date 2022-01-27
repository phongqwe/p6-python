from typing import Union, Optional

from bicp_document_structure.report.error.ErrorHeader import ErrorHeader
from bicp_document_structure.report.error.ErrorReport import ErrorReport

errPrefix = "workbookError_"

class WorkbookErrors:
    class WorksheetAlreadyExist:
        header = ErrorHeader(errPrefix+"1","worksheet already exist")
        class Data:
            def __init__(self,nameOrIndex: Union[str, int]):
                self.name=None
                self.index=None
                if isinstance(nameOrIndex,str):
                    self.name = nameOrIndex
                if isinstance(nameOrIndex, int):
                    self.index=nameOrIndex
    @staticmethod
    def toException(errReport:ErrorReport)->Optional[Exception]:
        if errReport.header == WorkbookErrors.WorksheetAlreadyExist.header:
            return ValueError(
                "{hd}\n{data}".format(
                    hd=str(WorkbookErrors.WorksheetAlreadyExist.header),
                    data=str(errReport.data)
                )
            )
        else:
            return None
