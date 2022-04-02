from abc import ABC
from pathlib import Path
from typing import Union, Optional

from bicp_document_structure.formula_translator.FormulaTranslator import FormulaTranslator
from bicp_document_structure.communication.proto.DocProtos_pb2 import WorkbookProto
from bicp_document_structure.util.report.error.ErrorReport import ErrorReport
from bicp_document_structure.util.result.Result import Result
from bicp_document_structure.workbook.WorkBook import Workbook
from bicp_document_structure.workbook.WorkbookJson import WorkbookJson
from bicp_document_structure.workbook.key.WorkbookKey import WorkbookKey
from bicp_document_structure.worksheet.Worksheet import Worksheet


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

    # def renameWorksheet(self, oldSheetNameOrIndex: str | int, newSheetName: str):
    #     return self._innerWorkbook.renameWorksheet(oldSheetNameOrIndex, newSheetName)
    #
    # def renameWorksheetRs(self, oldSheetNameOrIndex: str | int, newSheetName: str) -> Result[None, ErrorReport]:
    #     return self._innerWorkbook.renameWorksheetRs(oldSheetNameOrIndex, newSheetName)

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

    def getWorksheetByName(self, name: str) -> Worksheet:
        return self._innerWorkbook.getWorksheetByName(name)

    def getWorksheetByIndex(self, index: int) -> Worksheet:
        return self._innerWorkbook.getWorksheetByIndex(index)

    def getWorksheet(self, nameOrIndex: Union[str, int]) -> Worksheet:
        return self._innerWorkbook.getWorksheet(nameOrIndex)

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

    def getWorksheetByNameOrNone(self, name: str) -> Worksheet | None:
        return self._innerWorkbook.getWorksheetByNameOrNone(name)

    def getWorksheetByIndexOrNone(self, index: int) -> Optional[Worksheet]:
        return self._innerWorkbook.getWorksheetByIndexOrNone(index)

    def getWorksheetOrNone(self, nameOrIndex: Union[str, int]) -> Optional[Worksheet]:
        return self._innerWorkbook.getWorksheetOrNone(nameOrIndex)

