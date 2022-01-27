import json
from typing import Union, Optional

from bicp_document_structure.util.JsonStrMaker import JsonStrMaker
from bicp_document_structure.util.report.error.ErrorHeader import ErrorHeader
from bicp_document_structure.util.report.error.ErrorReport import ErrorReport
from bicp_document_structure.workbook.WorkbookKey import WorkbookKey

__errPrefix = "appErrors_"

def errPrefix():
    return __errPrefix

class AppErrors:
    class WorkbookAlreadyExist:
        header = ErrorHeader(errPrefix()+"1","workbook already exist")
        class Data:
            def __init__(self,nameOrIndexOrKey: Union[str, int, WorkbookKey]):
                if isinstance(nameOrIndexOrKey,str):
                    self.name = nameOrIndexOrKey
                if isinstance(nameOrIndexOrKey, int):
                    self.index=nameOrIndexOrKey
                if isinstance(nameOrIndexOrKey, WorkbookKey):
                    self.key = nameOrIndexOrKey

    class WorkbookNotExist:
        header = ErrorHeader(errPrefix() + "0", "workbook does not exist")
        class Data(JsonStrMaker):
            def __init__(self, nameOrIndexOrKey: Union[str, int, WorkbookKey]):
                self.name = None
                self.index = None
                self.key=None

                if isinstance(nameOrIndexOrKey, str):
                    self.name: str = nameOrIndexOrKey
                if isinstance(nameOrIndexOrKey, int):
                    self.index = nameOrIndexOrKey
                if isinstance(nameOrIndexOrKey, WorkbookKey):
                    self.key = nameOrIndexOrKey
            def __str__(self):
                if self.index is not None:
                    return "Workbook at index: "+str(self.index)
                if self.name is not None:
                    return "Workbook named "+ self.name
                if self.key is not None:
                    return "Workbook at key:\n"+str(self.key)
                return ""
            def jsonStr(self):
                return json.dumps(self.__dict__)

    @staticmethod
    def toException(errReport: ErrorReport)->Optional[Exception]:
        if errReport.header == AppErrors.WorkbookNotExist.header:
            return ValueError(
                "{hd}\n{data}".format(
                    hd=str(AppErrors.WorkbookNotExist.header),
                    data=str(errReport.data)
                )
            )
        else:
            return None