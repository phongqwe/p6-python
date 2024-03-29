from pathlib import Path
from typing import Union, Optional

from com.qxdzbc.p6.util.report.error.ErrorReport import ErrorReport
from com.qxdzbc.p6.util.result.Result import Result
from com.qxdzbc.p6.workbook.WorkBook import Workbook
from com.qxdzbc.p6.workbook.key.WorkbookKey import WorkbookKey
from com.qxdzbc.p6.worksheet.Worksheet import Worksheet


class WorkbookWrapper(Workbook):

    def __init__(self, innerWorkbook: Workbook):
        self._innerWorkbook = innerWorkbook

    def renameWorksheetRs(self, oldName: str, ws: Worksheet) -> Result[None, ErrorReport]:
        return self.rootWorkbook.renameWorksheetRs(oldName, ws)

    def makeSavableCopy(self) -> 'Workbook':
        return self.rootWorkbook.makeSavableCopy()

    @property
    def rootWorkbook(self) -> 'Workbook':
        return self._innerWorkbook.rootWorkbook

    def renameWorksheet(self, oldName: str, ws: Worksheet):
        self.rootWorkbook.renameWorksheet(oldName, ws)

    def addWorksheetRs(self, ws: Worksheet) -> Result[None, ErrorReport]:
        return self.rootWorkbook.addWorksheetRs(ws)

    @property
    def path(self) -> Path:
        return self.rootWorkbook.path

    @property
    def worksheets(self) -> list[Worksheet]:
        return self.rootWorkbook.worksheets

    @property
    def key(self) -> WorkbookKey:
        return self.rootWorkbook.key

    @key.setter
    def key(self, newKey: WorkbookKey):
        self.rootWorkbook.key = newKey

    @property
    def activeWorksheet(self) -> Optional[Worksheet]:
        return self.rootWorkbook.activeWorksheet

    @property
    def wsCount(self) -> int:
        return self.rootWorkbook.wsCount

    @property
    def name(self) -> str:
        return self.rootWorkbook.name

    @name.setter
    def name(self, newName):
        self.rootWorkbook.name = newName

    def createNewWorksheetRs(self, newSheetName: Optional[str] = None) -> Result[Worksheet, ErrorReport]:
        return self.rootWorkbook.createNewWorksheetRs(newSheetName)

    def removeWorksheetByNameRs(self, sheetName: str) -> Result[Worksheet, ErrorReport]:
        return self.rootWorkbook.removeWorksheetByNameRs(sheetName)

    def removeWorksheetByIndexRs(self, index: int) -> Result[Worksheet, ErrorReport]:
        return self.rootWorkbook.removeWorksheetByIndexRs(index)

    def setActiveWorksheetRs(self, indexOrName: Union[int, str]) -> Result[Worksheet, ErrorReport]:
        return self.rootWorkbook.setActiveWorksheetRs(indexOrName)

    def isEmpty(self) -> bool:
        return self.rootWorkbook.isEmpty()

    @property
    def innerWorkbook(self):
        return self._innerWorkbook

    def __eq__(self, o: object) -> bool:
        if isinstance(o, WorkbookWrapper):
            return self._innerWorkbook == o._innerWorkbook
        elif isinstance(o, Workbook):
            return self._innerWorkbook == o
        else:
            return False

    def getWorksheetByNameRs(self, name: str) -> Result[Worksheet, ErrorReport]:
        return self.rootWorkbook.getWorksheetByNameRs(name)

    def getWorksheetByIndexRs(self, index: int) -> Result[Worksheet, ErrorReport]:
        return self.rootWorkbook.getWorksheetByIndexRs(index)

    def getWorksheetRs(self, nameOrIndex: Union[str, int]) -> Result[Worksheet, ErrorReport]:
        return self.rootWorkbook.getWorksheetRs(nameOrIndex)
