from pathlib import Path
from typing import Optional, Union

from bicp_document_structure.workbook.WorkBook import Workbook
from bicp_document_structure.workbook.key.WorkbookKey import WorkbookKey


class WorkbookContainer:

    @property
    def bookCount(self):
        raise NotImplementedError()

    def getWorkbook(self, key: Union[int,str,WorkbookKey]) -> Optional[Workbook]:
        raise NotImplementedError()

    def getWorkbookByIndex(self, index: int):
        raise NotImplementedError()

    def getWorkbookByName(self, name: str):
        raise NotImplementedError()

    def getWorkbookByPath(self, path: Path):
        raise NotImplementedError()

    def getWorkbookByKey(self, fileInfo:WorkbookKey):
        raise NotImplementedError()

    # def createNewWorkbook(self, workbookName: str):
    #     raise NotImplementedError()

    def removeWorkbook(self, indexOrKey: Union[int, str, WorkbookKey]):
        raise NotImplementedError()

    def isEmpty(self) -> bool:
        raise NotImplementedError()

    def isNotEmpty(self) -> bool:
        return not self.isEmpty()

    def addWorkbook(self,workbook:Workbook):
        raise NotImplementedError()

    def books(self)->list[Workbook]:
        raise NotImplementedError()

    def clear(self):
        raise NotImplementedError()
