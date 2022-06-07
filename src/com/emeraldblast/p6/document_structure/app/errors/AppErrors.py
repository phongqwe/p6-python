import json
from typing import Union

from com.emeraldblast.p6.document_structure.util.report.ReportJsonStrMaker import ReportJsonStrMaker
from com.emeraldblast.p6.document_structure.util.report.error.ErrorHeader import ErrorHeader
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.emeraldblast.p6.document_structure.workbook.key.WorkbookKey import WorkbookKey

APPErr = "BE_AppErrors_"

def errPrefix():
    return APPErr

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
            def __str__(self):
                if self.index is not None:
                    return "Workbook at index: "+str(self.index)
                if self.name is not None:
                    return "Workbook named "+ self.name
                if self.key is not None:
                    return "Workbook at key:\n"+str(self.key)
                return ""

        @staticmethod
        def report(nameOrIndexOrKey: Union[str, int, WorkbookKey])->ErrorReport:
            data = AppErrors.WorkbookAlreadyExist.Data(nameOrIndexOrKey)
            return ErrorReport(
                header = ErrorHeader(errPrefix()+"1",f"workbook already exist.\n{str(data)}"),
                data = data
            )

    class WorkbookNotExist:
        header = ErrorHeader(errPrefix() + "0", "workbook does not exist")

        class Data(ReportJsonStrMaker):
            def __init__(self, nameOrIndexOrKey: Union[str, int, WorkbookKey]):
                self.wbName = None
                self.wbIndex = None
                self.wbKey=None

                if isinstance(nameOrIndexOrKey, str):
                    self.wbName: str = nameOrIndexOrKey
                if isinstance(nameOrIndexOrKey, int):
                    self.wbIndex = nameOrIndexOrKey
                if isinstance(nameOrIndexOrKey, WorkbookKey):
                    self.wbKey = nameOrIndexOrKey
            def __str__(self):
                if self.wbIndex is not None:
                    return "Workbook at index: "+str(self.wbIndex)
                if self.wbName is not None:
                    return "Workbook named "+ self.wbName
                if self.wbKey is not None:
                    return "Workbook at key:\n"+str(self.wbKey)
                return ""
            def reportJsonStr(self):
                return json.dumps(self.__dict__)

        @staticmethod
        def report(nameOrIndexOrKey: Union[str, int, WorkbookKey] = ""):
            data = AppErrors.WorkbookNotExist.Data(nameOrIndexOrKey)
            header = ErrorHeader(errPrefix() + "0", f"workbook does not exist.\n{str(data)}")
            return ErrorReport(
                header = header,
                data = data
            )
