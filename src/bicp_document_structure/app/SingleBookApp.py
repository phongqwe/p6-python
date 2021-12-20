from typing import Union, Optional

from bicp_document_structure.app.App import App
from bicp_document_structure.workbook.WorkBook import Workbook
from bicp_document_structure.workbook.WorkbookImp import WorkbookImp


class SingleBookApp(App):

    def __init__(self):
        wb = WorkbookImp("Book1")
        wb.createNewSheet("Sheet1")
        wb.setActiveSheet(0)
        self.__book = wb


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