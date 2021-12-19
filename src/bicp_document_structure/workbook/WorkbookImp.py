from collections import OrderedDict as ODict
from typing import List, Union, Optional, OrderedDict

from bicp_document_structure.sheet.Worksheet import Worksheet
from bicp_document_structure.sheet.WorksheetImp import WorksheetImp
from bicp_document_structure.util.Util import typeCheck
from bicp_document_structure.workbook.WorkBook import Workbook


class WorkbookImp(Workbook):

    def __init__(self, name, sheetDict: OrderedDict = None):
        self.__name = name

        if sheetDict is None:
            sheetDict = ODict()
        else:
            typeCheck(sheetDict, "sheetDict", OrderedDict)
        self.__sheetDict = sheetDict

    @staticmethod
    def fromSheets(wbName: str, sheetList: List[Worksheet]):
        sheetDict = ODict()
        for sheet in sheetList:
            sheetDict[sheet.name] = sheet
        return WorkbookImp(wbName, sheetDict)

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
    def activeSheet(self) -> Optional[Worksheet]:
        raise NotImplementedError()

    def isEmpty(self) -> bool:
        return self.sheetCount == 0

    def getSheetByName(self, name: str) -> Optional[Worksheet]:
        typeCheck(name, "name", str)
        if name in self.__sheetDict.keys():
            return self.__sheetDict[name]
        else:
            return None

    def getSheetByIndex(self, index: int) -> Optional[Worksheet]:
        typeCheck(index, "index", int)
        if 0 <= index < self.sheetCount:
            rt: Worksheet = list(self.__sheetDict.items())[index][1]
            return rt
        else:
            return None

    def getSheet(self, nameOrIndex: Union[str, int]) -> Optional[Worksheet]:
        if isinstance(nameOrIndex, str):
            return self.getSheetByName(nameOrIndex)
        elif isinstance(nameOrIndex, int):
            return self.getSheetByIndex(nameOrIndex)
        else:
            raise ValueError(
                "nameOrIndex is of type {t}. nameOrIndex must be string or int.".format(t=str(type(nameOrIndex))))

    @property
    def sheetCount(self) -> int:
        return len(self.__sheetDict)

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, newName: str):
        self.__name = newName

    def createNewSheet(self, newSheetName) -> Worksheet:
        if newSheetName in self.__sheetDict.keys():
            raise ValueError(
                "Can't create new sheet {sname} because sheet {sname} already exist".format(sname=newSheetName))
        else:
            newSheet = WorksheetImp(newSheetName)
            self.__sheetDict[newSheetName] = newSheet
            return newSheet

    def removeSheetByName(self, sheetName: str) -> Optional[Worksheet]:
        typeCheck(sheetName, "sheetName", str)
        if sheetName in self.__sheetDict.keys():
            rt: Worksheet = self.__sheetDict[sheetName]
            del self.__sheetDict[sheetName]
            return rt
        else:
            return None

    def removeSheetByIndex(self, index: int) -> Optional[Worksheet]:
        typeCheck(index, "index", int)
        if 0 <= index < len(self.__sheetDict):
            name: str = list(self.__sheetDict.items())[index][0]
            return self.removeSheetByName(name)
        else:
            return None

    def removeSheet(self, nameOrIndex: Union[str, int]) -> Optional[Worksheet]:
        if isinstance(nameOrIndex, str):
            return self.removeSheetByName(nameOrIndex)

        if isinstance(nameOrIndex, int):
            return self.removeSheetByIndex(nameOrIndex)
        raise ValueError("nameOrIndex must either be a string or a number")
