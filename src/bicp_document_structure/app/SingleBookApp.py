from typing import Union, Optional

from bicp_document_structure.app.App import App
from bicp_document_structure.app.workbook_container.WorkbookContainer import WorkbookContainer
from bicp_document_structure.cell.Cell import Cell
from bicp_document_structure.event.P6Event import P6Event
from bicp_document_structure.workbook.WorkBook import Workbook
from bicp_document_structure.workbook.WorkbookImp import WorkbookImp
from bicp_document_structure.workbook.WorkbookKey import WorkbookKey
from bicp_document_structure.worksheet.Worksheet import Worksheet


class SingleBookApp(App):

    """
    temporary imp of App interface
    """

    def __init__(self):
        wb = WorkbookImp("Book1", onCellChange =self.onCellMutation)
        wb.createNewWorksheet("Sheet1")
        wb.setActiveWorksheet(0)
        self.__book = wb

    def onCellMutation(self, workbook: Workbook,
                       worksheet:Worksheet,
                       cell: Cell,
                       mutationEvent: P6Event):
        pass


    @property
    def activeSheet(self):
        return self.activeWorkbook.activeWorksheet

    @property
    def activeWorkbook(self) -> Optional[Workbook]:
        return self.__book

    def getWorkbookByIndex(self, index: int) -> Optional[Workbook]:
        return self.__book

    def hasNoWorkbook(self) -> bool:
        return False

    def setActiveWorkbook(self, indexOrName: Union[int, str]):
        raise NotImplementedError()

    def createNewWorkbook(self, name: Optional[str] = None) -> Workbook:
        pass

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

    def getWorkbook(self, key: Union[str, int, WorkbookKey]) -> Optional[Workbook]:
        return self.__book

    def getWorkbookByKey(self, key: WorkbookKey) -> Optional[Workbook]:
        return self.__book



