import json
from abc import ABC
from pathlib import Path
from typing import Optional, Union

from com.qxdzbc.p6.util.CanCheckEmpty import CanCheckEmpty
from com.qxdzbc.p6.util.ToProto import ToProto
from com.qxdzbc.p6.util.report.error.ErrorReport import ErrorReport
from com.qxdzbc.p6.util.result.Result import Result
from com.qxdzbc.p6.util.result.Results import Results
from com.qxdzbc.p6.workbook.key.WorkbookKey import WorkbookKey
from com.qxdzbc.p6.worksheet.Worksheet import Worksheet
from com.qxdzbc.p6.proto.DocProtos_pb2 import WorkbookProto


class Workbook(CanCheckEmpty, ToProto[WorkbookProto], ABC):

    def isSimilar(self, o: object) -> bool:
        if isinstance(o, Workbook):
            c1 = self.key == o.key,
            c2 = len(self.worksheets) == len(o.worksheets)
            c3 = True
            for i in range(len(self.worksheets)):
                if not self.worksheets[i].compareContent(o.worksheets[i]):
                    c3 = False
                    break
            return c1 and c2 and c3
        else:
            return False

    def makeSavableCopy(self) -> 'Workbook':
        """create a copy instance that is fit for being saved to files"""
        raise NotImplementedError()

    @property
    def rootWorkbook(self) -> 'Workbook':
        raise NotImplementedError()

    def getIndexOfWorksheet(self, sheetName: str) -> int:
        for (index, sheet) in enumerate(self.worksheets):
            if sheet.name == sheetName:
                return index
        return -1

    def toProtoObj(self) -> WorkbookProto:
        # rootWb = self.rootWorkbook
        rt = WorkbookProto()
        rt.key.CopyFrom(self.key.toProtoObj())
        sheets = []
        for sheet in self.worksheets:
            sheets.append(sheet.toProtoObj())
        rt.worksheet.extend(sheets)
        scriptProtos = []
        for script in self.allScripts:
            scriptProtos.append(script.toProtoObj())
        rt.scripts.extend(scriptProtos)
        return rt

    def haveSheet(self, sheetName: str) -> bool:
        return self.getWorksheetOrNone(sheetName) is not None

    def reRun(self, refreshScript: bool = False):
        """rerun all worksheet in this workbook"""
        raise NotImplementedError()

    @property
    def worksheets(self) -> list[Worksheet]:
        """return a list of all sheet in this workbook"""
        raise NotImplementedError()

    @property
    def key(self) -> WorkbookKey:
        raise NotImplementedError()

    @key.setter
    def key(self, newKey: WorkbookKey):
        raise NotImplementedError()

    @property
    def activeWorksheet(self) -> Optional[Worksheet]:
        raise NotImplementedError()

    def setActiveWorksheetRs(self, indexOrName: Union[int, str]) -> Result[Worksheet, ErrorReport]:
        raise NotImplementedError()

    def setActiveWorksheet(self, indexOrName: Union[int, str]) -> Worksheet:
        rs = self.setActiveWorksheetRs(indexOrName)
        return Results.extractOrRaise(rs)

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

    def getWorksheetByNameOrNone(self, name: str) -> Optional[Worksheet]:
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
    def wsCount(self) -> int:
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

    def createNewWorksheet(self, newSheetName: Optional[str] = None) -> Worksheet:
        """
        add a new empty sheet to this workbook
        :param newSheetName: name of the new sheet
        :return the new worksheet
        :raise ValueError if the newSheetName already exists
        """
        createRs = self.createNewWorksheetRs(newSheetName)
        return Results.extractOrRaise(createRs)

    def createNewWorksheetRs(self, newSheetName: Optional[str] = None) -> Result[Worksheet, ErrorReport]:
        """
        add a new empty sheet to this workbook
        :param newSheetName: name of the new sheet
        :return Result object containing the new worksheet or ErrorRepor
        """
        raise NotImplementedError()

    def removeAllWorksheetRs(self)->Result[None,ErrorReport]:
        raise NotImplementedError()

    def removeAllWorksheet(self):
        rs = self.removeAllWorksheetRs()
        rs.getOrRaise()

    def removeWorksheetByName(self, sheetName: str) -> Worksheet:
        """ remove sheet by name. If the target sheet does not exist, simply return"""
        removeRs = self.removeWorksheetByNameRs(sheetName)
        return Results.extractOrRaise(removeRs)

    def removeWorksheetByIndex(self, index: int) -> Worksheet:
        """ remove sheet by index. If the target sheet does not exist, simply return"""
        removeRs = self.removeWorksheetByIndexRs(index)
        return Results.extractOrRaise(removeRs)

    def removeWorksheet(self, nameOrIndex: Union[str, int]) -> Worksheet:
        """ remove sheet by either index or name. If the target sheet does not exist, simply return"""
        removeRs = self.removeWorksheetRs(nameOrIndex)
        return Results.extractOrRaise(removeRs)

    def removeWorksheetByNameRs(self, sheetName: str) -> Result[Worksheet, ErrorReport]:
        """ remove sheet by name. If the target sheet does not exist, simply return"""
        raise NotImplementedError()

    def removeWorksheetByIndexRs(self, index: int) -> Result[Worksheet, ErrorReport]:
        """ remove sheet by index. If the target sheet does not exist, simply return"""
        raise NotImplementedError()

    def removeWorksheetRs(self, nameOrIndex: Union[str, int]) -> Result[Worksheet, ErrorReport]:
        """ remove sheet by either index or name. If the target sheet does not exist, simply return"""
        if isinstance(nameOrIndex, str):
            return self.removeWorksheetByNameRs(nameOrIndex)
        if isinstance(nameOrIndex, int):
            return self.removeWorksheetByIndexRs(nameOrIndex)
        raise ValueError("nameOrIndex must either be a string or a number")

    def addWorksheet(self, ws: Worksheet):
        addRs = self.addWorksheetRs(ws)
        if addRs.isOk():
            return
        else:
            raise addRs.err.toException()

    def renameWorksheet(self, oldName: str, ws: Worksheet):
        raise NotImplementedError()
    
    def renameWorksheetRs(self, oldName: str, ws: Worksheet)->Result[None, ErrorReport]:
        raise NotImplementedError()

    def addWorksheetRs(self, ws: Worksheet) -> Result[None, ErrorReport]:
        raise NotImplementedError()

    def summary(self) -> str:
        """return a summary of this workbook"""
        rt = ""
        for (i, sheet) in enumerate(self.worksheets):
            rt += "{num}. {sheetName}\n".format(
                num = str(i),
                sheetName = sheet.name
            )
        if not rt:
            rt = "empty book"
        return rt

    def printSummary(self):
        print(self.summary())

    def __str__(self):
        return self.summary()
