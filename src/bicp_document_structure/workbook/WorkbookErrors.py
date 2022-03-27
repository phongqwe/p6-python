import json
from typing import Union, Optional

from bicp_document_structure.util.ToRepStr import ToRepStr
from bicp_document_structure.util.report.error.ErrorHeader import ErrorHeader
from bicp_document_structure.util.report.error.ErrorReport import ErrorReport

WBErr = "WBErr"


class WorkbookErrors:
    class WorksheetAlreadyExist:
        header = ErrorHeader(f"{WBErr}1", "worksheet already exist")
        class Data(ToRepStr):
            def __init__(self, nameOrIndex: Union[str, int]):
                self.name = None
                self.index = None
                if isinstance(nameOrIndex, str):
                    self.name = nameOrIndex
                if isinstance(nameOrIndex, int):
                    self.index = nameOrIndex

            def repStr(self)->str:
                if self.name is not None:
                    return f"Can't create worksheet \"{self.name}\". It already exists"
                else:
                    return "Can't create new worksheet"

    class WorksheetNotExist:
        header = ErrorHeader(f"{WBErr}2", "worksheet not exist")

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