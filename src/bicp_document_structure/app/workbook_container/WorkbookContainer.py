from pathlib import Path
from typing import Optional, Union

from bicp_document_structure.workbook.WorkBook import Workbook
from bicp_document_structure.workbook.WorkbookFileInfo import WorkbookFileInfo


class WorkbookContainer:
    def getWorkbook(self, key: WorkbookFileInfo) -> Optional[Workbook]:
        raise NotImplementedError()

    def getWorkbookByIndex(self, index: int):
        raise NotImplementedError()

    def getWorkbookByName(self, name: str):
        raise NotImplementedError()

    def getWorkbookByPath(self, path: Path):
        raise NotImplementedError()

    def getWorkbookByFileInfo(self,fileInfo:WorkbookFileInfo):
        raise NotImplementedError()

    def createNewWorkbook(self, workbookName: str):
        raise NotImplementedError()

    def removeWorkbook(self, indexOrKey: Union[int, WorkbookFileInfo]):
        raise NotImplementedError()

    def isEmpty(self) -> bool:
        raise NotImplementedError()

    def isNotEmpty(self) -> bool:
        return not self.isEmpty()

    @property
    def bookCount(self):
        raise NotImplementedError()
