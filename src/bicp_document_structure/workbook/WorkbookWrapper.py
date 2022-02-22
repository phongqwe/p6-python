from abc import ABC
from typing import Union, Optional

from bicp_document_structure.util.report.error.ErrorReport import ErrorReport
from bicp_document_structure.util.result.Result import Result
from bicp_document_structure.workbook.WorkBook import Workbook
from bicp_document_structure.workbook.WorkbookKey import WorkbookKey
from bicp_document_structure.worksheet.Worksheet import Worksheet


class WorkbookWrapper(Workbook,ABC):

    def __init__(self,innerWorkbook:Workbook):
        self._innerWorkbook = innerWorkbook

    @property
    def worksheets(self) -> list[Worksheet]:
        return self._innerWorkbook.worksheets

    @property
    def workbookKey(self) -> WorkbookKey:
        return self._innerWorkbook.workbookKey

    @property
    def activeWorksheet(self) -> Optional[Worksheet]:
        return self._innerWorkbook.activeWorksheet

    def setActiveWorksheet(self, indexOrName: Union[int, str]):
        self._innerWorkbook.setActiveWorksheet(indexOrName)

    def getWorksheetByName(self, name: str) -> Optional[Worksheet]:
        return self._innerWorkbook.getWorksheetByName(name)

    def getWorksheetByIndex(self, index: int) -> Optional[Worksheet]:
        return self._innerWorkbook.getWorksheetByIndex(index)

    def getWorksheet(self, nameOrIndex: Union[str, int]) -> Optional[Worksheet]:
        return self._innerWorkbook.getWorksheet(nameOrIndex)

    @property
    def sheetCount(self) -> int:
        return self._innerWorkbook.sheetCount

    @property
    def name(self) -> str:
        return self._innerWorkbook.name

    def createNewWorksheetRs(self, newSheetName: Optional[str] = None) -> Result[Worksheet, ErrorReport]:
        return self._innerWorkbook.createNewWorksheetRs(newSheetName)

    def removeWorksheetByNameRs(self, sheetName: str) -> Result[Worksheet, ErrorReport]:
        return self._innerWorkbook.removeWorksheetByNameRs(sheetName)

    def removeWorksheetByIndexRs(self, index: int) -> Result[Worksheet, ErrorReport]:
        return self._innerWorkbook.removeWorksheetByIndexRs(index)

    def removeWorksheetRs(self, nameOrIndex: Union[str, int]) -> Result[Worksheet, ErrorReport]:
        return self._innerWorkbook.removeWorksheetRs(nameOrIndex)

    def toJsonDict(self) -> dict:
        return self._innerWorkbook.toJsonDict()

    def isEmpty(self) -> bool:
        return self._innerWorkbook.isEmpty()