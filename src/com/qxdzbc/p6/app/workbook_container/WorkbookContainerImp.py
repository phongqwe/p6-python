from pathlib import Path
from typing import Union, Optional

from com.qxdzbc.p6.app.workbook_container.WorkbookContainer import WorkbookContainer
from com.qxdzbc.p6.util.WithSize import WithSize
from com.qxdzbc.p6.workbook.WorkBook import Workbook
from com.qxdzbc.p6.workbook.key.WorkbookKey import WorkbookKey


class WorkbookContainerImp(WorkbookContainer,WithSize):

    def __init__(self, wbDict: dict[WorkbookKey,Workbook] = None):
        if wbDict is None:
            wbDict = {}
        self.__wbDict:dict[WorkbookKey,Workbook] = wbDict

    ### >> WorkbookContainer << ###

    def addWorkbook(self, workbook: Workbook):
        self.__wbDict[workbook.key] = workbook

    def books(self) -> list[Workbook]:
        return list(self.__wbDict.values())

    def clear(self):
        self.__wbDict.clear()

    def getWorkbook(self, key: Union[int,str,WorkbookKey]) -> Optional[Workbook]:
        if isinstance(key,int):
            return self.getWorkbookByIndex(key)
        if isinstance(key,str):
            return self.getWorkbookByName(key)
        if isinstance(key,WorkbookKey):
            return self.getWorkbookByKey(key)

    def getWorkbookByIndex(self, index: int)-> Optional[Workbook]:
        if 0 <= index < len(self.__wbDict):
            rt= list(self.__wbDict.items())[index][1]
            return rt
        else:
            # raise ValueError("Workbook at {i} does not exist".format(i=index))
            return None

    def getWorkbookByName(self, name: str):
        for k,v in self.__wbDict.items():
            if k.fileName == name:
                return v
        # raise ValueError("Workbook named {n} does not exist".format(n=name))
        return None

    def getWorkbookByPath(self, path: Path):
        for k,v in self.__wbDict.items():
            if k.filePath == path:
                return v
        # raise ValueError("Workbook at path {n} does not exist".format(n=str(path)))
        return None

    def getWorkbookByKey(self, fileInfo: WorkbookKey):
        key = fileInfo
        if key in self.__wbDict.keys():
            return self.__wbDict[key]
        else:
            # raise ValueError(
            #     "{wbn} does not exist (file = {fd})".format(wbn=key.fileName, fd=key.filePath))
            return None

    def removeWorkbook(self, indexOrKey: Union[int, str, WorkbookKey]):
        wb = self.getWorkbook(indexOrKey)
        if wb is not None:
            del self.__wbDict[wb.key]


    def isEmpty(self) -> bool:
        return len(self.__wbDict) == 0

    @property
    def bookCount(self):
        return self.size

    @property
    def size(self) -> int:
        return len(self.__wbDict)
