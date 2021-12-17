from com.github.xadkile.bicp.doc.data_structure.sheet.WorksheetImp import WorksheetImp
from com.github.xadkile.bicp.doc.data_structure.workbook.WorkBook import Workbook


class WorkbookImp(Workbook):

    def __init__(self,name,sheetDict:dict = None):
        self.__name = name
        if sheetDict is None:
            sheetDict = {}
        self.__sheetDict = sheetDict
        self.__orderDict = self.__makeOrderDict(sheetDict)

    def __makeOrderDict(self,sheetDict:dict)->dict:
        o = 0
        rt = {}
        for k, v in list(sheetDict.items()):
            rt[o] = k
            o += 1
        return rt

    ### >> Workbook << ###
    @property
    def sheetCount(self) -> int:
        return len(self.__sheetDict)

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, newName: str):
        self.__name = newName

    def createNewSheet(self, newSheetName):
        self.__sheetDict[newSheetName] = WorksheetImp()

    def removeSheetByName(self, sheetName: str):
        if sheetName in self.__sheetDict.keys():
            del self.__sheetDict[sheetName]

    def removeSheetByIndex(self, index: int):
        if index in self.__orderDict.keys():
            sheetName = self.__sheetDict[index]
            self.removeSheetByName(sheetName)

    def removeSheet(self, nameOrIndex):
        if isinstance(nameOrIndex,str):
            self.removeSheetByName(nameOrIndex)
            return
        if isinstance(nameOrIndex,int):
            self.removeSheetByIndex(nameOrIndex)
            return
        raise ValueError("nameOrIndex must either be a string or a number")



