import json
from abc import ABC
from pathlib import Path
from typing import Optional, Union

from com.emeraldblast.p6.document_structure.formula_translator.FormulaTranslator import FormulaTranslator
from com.emeraldblast.p6.document_structure.util.CanCheckEmpty import CanCheckEmpty
from com.emeraldblast.p6.document_structure.util.ToJson import ToJson
from com.emeraldblast.p6.document_structure.util.ToProto import ToProto
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.emeraldblast.p6.document_structure.util.result.Result import Result
from com.emeraldblast.p6.document_structure.util.result.Results import Results
from com.emeraldblast.p6.document_structure.workbook.WorkbookJson import WorkbookJson
from com.emeraldblast.p6.document_structure.workbook.key.WorkbookKey import WorkbookKey
from com.emeraldblast.p6.document_structure.worksheet.Worksheet import Worksheet
from com.emeraldblast.p6.proto.DocProtos_pb2 import WorkbookProto


class Workbook(ToJson, CanCheckEmpty, ToProto[WorkbookProto], ABC):
    # Worksheet = WS.Worksheet
    def getIndexOfWorksheet(self, sheetName: str) -> int:
        for (index, sheet) in enumerate(self.worksheets):
            if sheet.name == sheetName:
                return index
        return -1

    def toProtoObj(self) -> WorkbookProto:
        rt = WorkbookProto()
        rt.workbookKey.CopyFrom(self.workbookKey.toProtoObj())
        sheets = []
        for sheet in self.worksheets:
            sheets.append(sheet.toProtoObj())
        rt.worksheet.extend(sheets)
        return rt

    def getTranslator(self, sheetName: str) -> FormulaTranslator:
        raise NotImplementedError()

    def haveSheet(self, sheetName: str) -> bool:
        return self.getWorksheetOrNone(sheetName) is not None

    def reRun(self):
        """rerun all worksheet in this workbook"""
        for sheet in self.worksheets:
            sheet.reRun()

    @property
    def worksheets(self) -> list[Worksheet]:
        """return a list of all sheet in this workbook"""
        raise NotImplementedError()

    @property
    def workbookKey(self) -> WorkbookKey:
        raise NotImplementedError()

    @workbookKey.setter
    def workbookKey(self, newKey: WorkbookKey):
        raise NotImplementedError()

    @property
    def activeWorksheet(self) -> Optional[Worksheet]:
        raise NotImplementedError()

    def setActiveWorksheet(self, indexOrName: Union[int, str]):
        raise NotImplementedError()

    def getWorksheetByName(self, name: str) -> Worksheet:
        """
        :param name: sheet name
        :return: the sheet having that name or None if no such sheet exists
        """
        return Results.extractOrRaise(self.getWorksheetByNameRs(name))

    def getWorksheetByNameRs(self, name: str) -> Result[Worksheet, ErrorReport]:
        raise NotImplementedError()

    def getWorksheetByIndexRs(self, index: int) -> Result[Worksheet, ErrorReport]:
        raise NotImplementedError()

    def getWorksheetRs(self, nameOrIndex: Union[str, int]) -> Result[Worksheet, ErrorReport]:
        raise NotImplementedError()

    def getWorksheetByNameOrNone(self, name: str) -> Worksheet | None:
        """
        :param name: sheet name
        :return: the sheet having that name or None if no such sheet exists
        """
        return Results.extractOrNone(self.getWorksheetByNameRs(name))

    def getWorksheetByIndex(self, index: int) -> Worksheet:
        """
        :param index: index of a sheet
        :return: the sheet at that index, or None if no such sheet exists
        """
        return Results.extractOrRaise(self.getWorksheetByIndexRs(index))

    def getWorksheetByIndexOrNone(self, index: int) -> Optional[Worksheet]:
        """
        :param index: index of a sheet
        :return: the sheet at that index, or None if no such sheet exists
        """
        return Results.extractOrNone(self.getWorksheetByIndexRs(index))

    def getWorksheetOrNone(self, nameOrIndex: Union[str, int]) -> Optional[Worksheet]:
        return Results.extractOrNone(self.getWorksheetRs(nameOrIndex))

    def getWorksheet(self, nameOrIndex: Union[str, int]) -> Worksheet:
        """
        get a sheet either by name or index
        :param nameOrIndex: name or index
        :return: the sheet at that index/name, or None if no such sheet exists
        """
        return Results.extractOrRaise(self.getWorksheetRs(nameOrIndex))

    @property
    def sheetCount(self) -> int:
        raise NotImplementedError()

    @property
    def name(self) -> str:
        raise NotImplementedError()

    @name.setter
    def name(self, newName: str):
        raise NotImplementedError()

    @property
    def path(self) -> Path:
        raise NotImplementedError()

    @path.setter
    def path(self, newPath: Path):
        raise NotImplementedError()

    def createNewWorksheet(self, newSheetName: Optional[str]) -> Worksheet:
        """
        add a new empty sheet to this workbook
        :param newSheetName: name of the new sheet
        :return the new worksheet
        :raise ValueError if the newSheetName already exists
        """
        createRs = self.createNewWorksheetRs(newSheetName)
        if createRs.isOk():
            return createRs.value
        else:
            raise createRs.err.toException()

    def createNewWorksheetRs(self, newSheetName: Optional[str] = None) -> Result[Worksheet, ErrorReport]:
        """
        add a new empty sheet to this workbook
        :param newSheetName: name of the new sheet
        :return Result object containing the new worksheet or ErrorRepor
        """
        raise NotImplementedError()

    def removeWorksheetByName(self, sheetName: str) -> Optional[Worksheet]:
        """ remove sheet by name. If the target sheet does not exist, simply return"""
        removeRs = self.removeWorksheetByNameRs(sheetName)
        if removeRs.isOk():
            return removeRs.value
        else:
            raise removeRs.err.toException()

    def removeWorksheetByIndex(self, index: int) -> Optional[Worksheet]:
        """ remove sheet by index. If the target sheet does not exist, simply return"""
        removeRs = self.removeWorksheetByIndexRs(index)
        if removeRs.isOk():
            return removeRs.value
        else:
            raise removeRs.err.toException()

    def removeWorksheet(self, nameOrIndex: Union[str, int]) -> Optional[Worksheet]:
        """ remove sheet by either index or name. If the target sheet does not exist, simply return"""
        removeRs = self.removeWorksheetRs(nameOrIndex)
        if removeRs.isOk():
            return removeRs.value
        else:
            raise removeRs.err.toException()

    def removeWorksheetByNameRs(self, sheetName: str) -> Result[Worksheet, ErrorReport]:
        """ remove sheet by name. If the target sheet does not exist, simply return"""
        raise NotImplementedError()

    def removeWorksheetByIndexRs(self, index: int) -> Result[Worksheet, ErrorReport]:
        """ remove sheet by index. If the target sheet does not exist, simply return"""
        raise NotImplementedError()

    def removeWorksheetRs(self, nameOrIndex: Union[str, int]) -> Result[Worksheet, ErrorReport]:
        """ remove sheet by either index or name. If the target sheet does not exist, simply return"""
        raise NotImplementedError()

    def addWorksheet(self, ws: Worksheet):
        addRs = self.addWorksheetRs(ws)
        if addRs.isOk():
            return
        else:
            raise addRs.err.toException()

    def updateSheetName(self, oldName: str, ws: Worksheet):
        raise NotImplementedError()

    def addWorksheetRs(self, ws: Worksheet) -> Result[None, ErrorReport]:
        raise NotImplementedError()

    def toJson(self) -> WorkbookJson:
        jsons = []
        for sheet in self.worksheets:
            jsons.append(sheet.toJson())
        pathJson = None
        if self.workbookKey.filePath is not None:
            pathJson = str(self.workbookKey.filePath)
        return WorkbookJson(self.name, pathJson, jsons)

    def summary(self) -> str:
        """return a list of sheet as string"""
        rt = ""
        for (i, sheet) in enumerate(self.worksheets):
            rt += "{num}. {sheetName}\n".format(
                num = str(i),
                sheetName = sheet.name
            )
        if not rt:
            rt = "empty book"
        print(rt)

    def reportJsonStr(self) -> str:
        return json.dumps(self.toJson().toJsonDict())

    def toJsonStrForSaving(self) -> str:
        return self.toJson().toJsonStrForSaving()
