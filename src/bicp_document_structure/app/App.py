from abc import ABC
from pathlib import Path
from typing import Optional, Union

from bicp_document_structure.app.run_result.RunResult import RunResult
from bicp_document_structure.app.workbook_container.WorkbookContainer import WorkbookContainer
from bicp_document_structure.workbook.WorkBook import Workbook
from bicp_document_structure.workbook.WorkbookKey import WorkbookKey
from bicp_document_structure.worksheet.Worksheet import Worksheet


class App(ABC):
    """
    this class represents the state of the app.
    """
    @property
    def wbContainer(self)->WorkbookContainer:
        raise NotImplementedError()

    @property
    def result(self) -> RunResult:
        raise NotImplementedError()

    @property
    def activeWorkbook(self) -> Optional[Workbook]:
        raise NotImplementedError()

    def setActiveWorkbook(self, indexOrNameOrKey: Union[int, str, WorkbookKey]):
        """
        Set workbook at indexOrName the active workbook.
        Should raise an exception if the indexOrName is invalid
        """
        raise NotImplementedError()

    @property
    def activeSheet(self)->Optional[Worksheet]:
        raise NotImplementedError()

    def getWorkbookByIndex(self, index: int) -> Optional[Workbook]:
        """:return workbook at an index"""
        raise NotImplementedError()

    def getWorkbookByName(self, name: str) -> Optional[Workbook]:
        """:return workbook at an index"""
        raise NotImplementedError()

    def getWorkbookByKey(self,key:WorkbookKey)->Optional[Workbook]:
        """:return workbook at a key"""
        raise NotImplementedError()

    def getWorkbook(self, key:Union[str,int,WorkbookKey])->Optional[Workbook]:
        """:return workbook at a key that is either a name, an index, or a WorkbookKey"""
        raise NotImplementedError()
    def hasNoWorkbook(self) -> bool:
        """
        :return: true if this app does not have any workbook
        """
        raise NotImplementedError()

    def createNewWorkBook(self, name: str):
        """create a new workbook, and add it to this app state"""
        raise NotImplementedError()

    def saveWorkbookAtPath(self, nameOrIndexOrKey: Union[int, str, WorkbookKey], filePath: Union[str,Path]):
        """
        save a workbook at nameOrIndex to a certain filePath, then update the workbook with that new path
        """
        raise NotImplementedError()

    def saveWorkbook(self, nameOrIndexOrKey: Union[int, str, WorkbookKey]):
        """save a workbook at nameOrIndex"""
        raise NotImplementedError()

    def loadWorkbook(self, filePath: str) -> bool:
        """load a workbook from a file path, and add it to this app state"""
        raise NotImplementedError()
