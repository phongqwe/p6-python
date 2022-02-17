from collections import OrderedDict as ODict
from pathlib import Path
from typing import Union, Optional, OrderedDict, Callable

from bicp_document_structure.cell.Cell import Cell
from bicp_document_structure.event.P6Event import P6Event
from bicp_document_structure.util.Util import typeCheck
from bicp_document_structure.util.report.error.ErrorReport import ErrorReport
from bicp_document_structure.util.result.Err import Err
from bicp_document_structure.util.result.Ok import Ok
from bicp_document_structure.util.result.Result import Result
from bicp_document_structure.workbook.WorkBook import Workbook
from bicp_document_structure.workbook.WorkbookErrors import WorkbookErrors
from bicp_document_structure.workbook.WorkbookKey import WorkbookKey
from bicp_document_structure.workbook.WorkbookKeyImp import WorkbookKeyImp
from bicp_document_structure.worksheet.Worksheet import Worksheet
from bicp_document_structure.worksheet.WorksheetImp import WorksheetImp


class WorkbookImp(Workbook):

    def __init__(self, name: str,
                 path: Path = None,
                 sheetDict: OrderedDict = None,
                 onCellMutation: Callable[[Workbook, Worksheet, Cell, P6Event], None] = None,
                 ):
        self.__onCellMutation: Optional[Callable[[Workbook, Worksheet, Cell, P6Event], None]] = onCellMutation
        self.__key = WorkbookKeyImp(name, path)
        if sheetDict is None:
            sheetDict = ODict()
        else:
            typeCheck(sheetDict, "sheetDict", OrderedDict)
        self.__sheetDict = sheetDict

        self.__activeSheet = None
        if self.sheetCount != 0:
            self.__activeSheet = list(self.__sheetDict.values())[0]
        self.__nameCount = 0

    @staticmethod
    def __makeOrderDict(sheetDict: dict) -> dict:
        o = 0
        rt = {}
        for k, v in list(sheetDict.items()):
            rt[o] = k
            o += 1
        return rt

    ### >> Workbook << ###

    @property
    def worksheets(self) -> list[Worksheet]:
        return list(self.__sheetDict.values())

    @property
    def workbookKey(self) -> WorkbookKey:
        return self.__key

    @workbookKey.setter
    def workbookKey(self, newKey: WorkbookKey):
        self.__key = newKey

    def setActiveWorksheet(self, indexOrName: Union[int, str]):
        sheet = self.getWorksheet(indexOrName)
        if sheet is not None:
            self.__activeSheet = sheet
        else:
            raise ValueError("{n} is invalid workbook index or workbook".format(n=indexOrName))

    @property
    def activeWorksheet(self) -> Optional[Worksheet]:
        if not self.isEmpty() and self.__activeSheet is None:
            self.__activeSheet = self.getWorksheetByIndex(0)
        return self.__activeSheet

    def isEmpty(self) -> bool:
        return self.sheetCount == 0

    def getWorksheetByName(self, name: str) -> Optional[Worksheet]:
        typeCheck(name, "name", str)
        if name in self.__sheetDict.keys():
            return self.__sheetDict[name]
        else:
            return None

    def getWorksheetByIndex(self, index: int) -> Optional[Worksheet]:
        typeCheck(index, "index", int)
        if 0 <= index < self.sheetCount:
            rt: Worksheet = list(self.__sheetDict.items())[index][1]
            return rt
        else:
            return None

    def getWorksheet(self, nameOrIndex: Union[str, int]) -> Optional[Worksheet]:
        if isinstance(nameOrIndex, str):
            return self.getWorksheetByName(nameOrIndex)
        elif isinstance(nameOrIndex, int):
            return self.getWorksheetByIndex(nameOrIndex)
        else:
            raise ValueError(
                "nameOrIndex is of type {t}. nameOrIndex must be string or int.".format(t=str(type(nameOrIndex))))

    @property
    def sheetCount(self) -> int:
        return len(self.__sheetDict)

    @property
    def name(self) -> str:
        return self.workbookKey.fileName

    @name.setter
    def name(self, newName: str):
        self.workbookKey = WorkbookKeyImp(newName, self.workbookKey.filePath)

    def createNewWorksheetRs(self, newSheetName: Optional[str]=None) -> Result[Worksheet, ErrorReport]:
        if newSheetName is None:
            newSheetName = "Sheet" + str(self.__nameCount)
            while self.getWorksheetByName(newSheetName) is not None:
                self.__nameCount += 1
                newSheetName = "Sheet" + str(self.__nameCount)
        else:
            if newSheetName in self.__sheetDict.keys():
                return Err(
                    ErrorReport(
                        header=WorkbookErrors.WorksheetAlreadyExist.header,
                        data=WorkbookErrors.WorksheetAlreadyExist.Data(newSheetName)
                    )
                )
        newSheet = WorksheetImp(name=newSheetName,
                                onCellMutation=self.__onCellChange)
        self.__sheetDict[newSheetName] = newSheet
        return Ok(newSheet)

    def __onCellChange(self,
                       worksheet: Worksheet,
                       cell: Cell,
                       mutationEvent: P6Event):
        if self.__onCellMutation is not None:
            self.__onCellMutation(self, worksheet, cell, mutationEvent)

    def removeWorksheetByNameRs(self, sheetName: str) -> Result[Worksheet, ErrorReport]:
        typeCheck(sheetName, "sheetName", str)
        if sheetName in self.__sheetDict.keys():
            rt: Worksheet = self.__sheetDict[sheetName]
            del self.__sheetDict[sheetName]
            return Ok(rt)
        else:
            return Err(
                ErrorReport(
                    header=WorkbookErrors.WorksheetAlreadyExist.header,
                    data=WorkbookErrors.WorksheetAlreadyExist.Data(sheetName),
                )
            )

    def removeWorksheetByIndexRs(self, index: int) -> Result[Worksheet, ErrorReport]:
        typeCheck(index, "index", int)
        if 0 <= index < len(self.__sheetDict):
            name: str = list(self.__sheetDict.items())[index][0]
            return self.removeWorksheetByNameRs(name)
        else:
            return Err(
                ErrorReport(
                    header=WorkbookErrors.WorksheetAlreadyExist.header,
                    data=WorkbookErrors.WorksheetAlreadyExist.Data(index),
                )
            )

    def removeWorksheetRs(self, nameOrIndex: Union[str, int]) -> Result[Worksheet, ErrorReport]:
        if isinstance(nameOrIndex, str):
            return self.removeWorksheetByNameRs(nameOrIndex)

        if isinstance(nameOrIndex, int):
            return self.removeWorksheetByIndexRs(nameOrIndex)

        raise ValueError("nameOrIndex must either be a string or a number")

