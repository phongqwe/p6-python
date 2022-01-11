from typing import Union, Optional

from bicp_document_structure.app.App import App
from bicp_document_structure.app.run_result.RunResult import RunResult
from bicp_document_structure.app.run_result.RunResultImp import RunResultImp
from bicp_document_structure.app.workbook_container.WorkbookContainer import WorkbookContainer
from bicp_document_structure.mutation.CellMutationEvent import CellMutationEvent
from bicp_document_structure.workbook.WorkBook import Workbook
from bicp_document_structure.workbook.WorkbookImp import WorkbookImp
from bicp_document_structure.workbook.WorkbookKey import WorkbookKey


class SingleBookApp(App):

    """
    temporary imp of App interface
    """

    def __init__(self):
        rr = RunResultImp()
        wb = WorkbookImp("Book1",onCellMutation=self.onCellMutation)
        wb.createNewSheet("Sheet1")
        wb.setActiveSheet(0)
        self.__book = wb
        self.__result = rr

    def onCellMutation(self, cell, mutationEvent):
        if mutationEvent == CellMutationEvent.DELETED:
            self.__result.addDeletedCell(None,"",cell.address)
        if mutationEvent == CellMutationEvent.NEW_SCRIPT or mutationEvent == CellMutationEvent.NEW_VALUE:
            self.__result.addMutatedCell(None,"",cell)


    @property
    def result(self) -> RunResult:
        return self.__result

    @property
    def activeSheet(self):
        return self.activeWorkbook.activeSheet

    @property
    def activeWorkbook(self) -> Optional[Workbook]:
        return self.__book

    def getWorkbookByIndex(self, index: int) -> Optional[Workbook]:
        return self.__book

    def hasNoWorkbook(self) -> bool:
        return False

    def setActiveWorkbook(self, indexOrName: Union[int, str]):
        raise NotImplementedError()

    def createNewWorkBook(self, name: str):
        raise NotImplementedError()

    def saveWorkbookAtPath(self, nameOrIndex: Union[int, str,WorkbookKey], filePath: str):
        raise NotImplementedError()

    @property
    def wbContainer(self) -> WorkbookContainer:
        pass

    def getWorkbookByName(self, name: str) -> Optional[Workbook]:
        pass

    def saveWorkbook(self, nameOrIndexOrKey: Union[int, str, WorkbookKey]):
        pass

    def loadWorkbook(self, filePath: str) -> bool:
        raise NotImplementedError()