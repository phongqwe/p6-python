import json
from typing import Union, Optional

from bicp_document_structure.util.report.error.ErrorHeader import ErrorHeader
from bicp_document_structure.util.report.error.ErrorReport import ErrorReport

errPrefix = "workbookError_"


class WorkbookErrors:
    class WorksheetAlreadyExist:
        header = ErrorHeader(errPrefix + "1", "worksheet already exist")

        class Data:
            def __init__(self, nameOrIndex: Union[str, int]):
                self.name = None
                self.index = None
                if isinstance(nameOrIndex, str):
                    self.name = nameOrIndex
                if isinstance(nameOrIndex, int):
                    self.index = nameOrIndex

            def __str__(self):
                return json.dumps(self.__dict__)
    class WorksheetNotExist:
        header = ErrorHeader(errPrefix + "2", "worksheet not exist")

        class Data:
            def __init__(self, nameOrIndex: Union[str, int]):
                self.name = None
                self.index = None
                if isinstance(nameOrIndex, str):
                    self.name = nameOrIndex
                if isinstance(nameOrIndex, int):
                    self.index = nameOrIndex

            def __str__(self):
                return json.dumps(self.__dict__)

    @staticmethod
    def toException(errReport: ErrorReport) -> Optional[Exception]:
        match errReport.header:
            case WorkbookErrors.WorksheetAlreadyExist.header:
                return ValueError(
                    "{hd}\n{data}".format(
                        hd=str(WorkbookErrors.WorksheetAlreadyExist.header),
                        data=str(errReport.data)
                    )
                )
            case WorkbookErrors.WorksheetNotExist.header:
                return ValueError(
                    "{hd}\n{data}".format(
                        hd = str(WorkbookErrors.WorksheetAlreadyExist.header),
                        data = str(errReport.data)
                    )
                )
            case _:
                return None
