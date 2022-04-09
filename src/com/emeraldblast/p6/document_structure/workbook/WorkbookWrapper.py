from pathlib import Path
from typing import Union, Optional

from com.emeraldblast.p6.document_structure.formula_translator.FormulaTranslator import FormulaTranslator
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.emeraldblast.p6.document_structure.util.result.Result import Result
from com.emeraldblast.p6.document_structure.workbook.WorkBook import Workbook
from com.emeraldblast.p6.document_structure.workbook.key.WorkbookKey import WorkbookKey
from com.emeraldblast.p6.document_structure.worksheet.Worksheet import Worksheet


class WorkbookWrapper(Workbook):

    def updateSheetName(self, oldName: str, ws: Worksheet):
        self._innerWorkbook.updateSheetName(oldName,ws)

    def addWorksheetRs(self, ws: Worksheet) -> Result[None, ErrorReport]:
        return self._innerWorkbook.addWorksheetRs(ws)

    def __init__(self,innerWorkbook:Workbook):
        self._innerWorkbook = innerWorkbook

    def getTranslator(self, sheetName: str) -> FormulaTranslator:
        return self._innerWorkbook.getTranslator(sheetName)

    @property
    def path(self) -> Path:
        return self._innerWorkbook.path

    @property
    def worksheets(self) -> list[Worksheet]:
        return self._innerWorkbook.worksheets

    @property
    def workbookKey(self) -> WorkbookKey:
        return self._innerWorkbook.workbookKey

    @workbookKey.setter
    def workbookKey(self,newKey:WorkbookKey):
        self._innerWorkbook.workbookKey = newKey

    @property
    def activeWorksheet(self) -> Optional[Worksheet]:
        return self._innerWorkbook.activeWorksheet

    def setActiveWorksheet(self, indexOrName: Union[int, str]):
        self._innerWorkbook.setActiveWorksheet(indexOrName)

    @property
    def sheetCount(self) -> int:
        return self._innerWorkbook.sheetCount

    @property
    def name(self) -> str:
        return self._innerWorkbook.name

    @name.setter
    def name(self,newName):
        self._innerWorkbook.name = newName

    def createNewWorksheetRs(self, newSheetName: Optional[str] = None) -> Result[Worksheet, ErrorReport]:
        return self._innerWorkbook.createNewWorksheetRs(newSheetName)

    def deleteWorksheetByNameRs(self, sheetName: str) -> Result[Worksheet, ErrorReport]:
        return self._innerWorkbook.deleteWorksheetByNameRs(sheetName)

    def deleteWorksheetByIndexRs(self, index: int) -> Result[Worksheet, ErrorReport]:
        return self._innerWorkbook.deleteWorksheetByIndexRs(index)

    def setActiveWorksheetRs(self, indexOrName: Union[int, str]) -> Result[Worksheet, ErrorReport]:
        return self._innerWorkbook.setActiveWorksheetRs(indexOrName)

    def toJsonDict(self) -> dict:
        return self._innerWorkbook.toJsonDict()

    def isEmpty(self) -> bool:
        return self._innerWorkbook.isEmpty()

    @property
    def innerWorkbook(self):
        return self._innerWorkbook

    def __eq__(self, o: object) -> bool:
        if isinstance(o,WorkbookWrapper):
            return self._innerWorkbook == o._innerWorkbook
        elif isinstance(o,Workbook):
            return self._innerWorkbook == o
        else:
            return False


    def getWorksheetByNameRs(self, name: str) -> Result[Worksheet, ErrorReport]:
        return self._innerWorkbook.getWorksheetByNameRs(name)

    def getWorksheetByIndexRs(self, index: int) -> Result[Worksheet, ErrorReport]:
        return self._innerWorkbook.getWorksheetByIndexRs(index)

    def getWorksheetRs(self, nameOrIndex: Union[str, int]) -> Result[Worksheet, ErrorReport]:
        return self._innerWorkbook.getWorksheetRs(nameOrIndex)


