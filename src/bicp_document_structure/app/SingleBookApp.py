from typing import Union, Optional

from bicp_document_structure.app.App import App
from bicp_document_structure.app.run_result.RunResult import RunResult
from bicp_document_structure.app.run_result.RunResultImp import RunResultImp
from bicp_document_structure.workbook.WorkBook import Workbook
from bicp_document_structure.workbook.WorkbookImp import WorkbookImp


class SingleBookApp(App):

    """
    temporary imp of App interface
    """

    def __init__(self):
        wb = WorkbookImp("Book1")
        wb.createNewSheet("Sheet1")
        wb.setActiveSheet(0)
        self.__book = wb
        self.__result = RunResultImp()

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

    def saveWorkbook(self, nameOrIndex: Union[int, str], filePath: str):
        raise NotImplementedError()

    def loadWorkbook(self, filePath: str) -> bool:
        raise NotImplementedError()