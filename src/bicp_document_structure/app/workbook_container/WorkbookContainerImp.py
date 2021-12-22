from collections import OrderedDict as OD
from pathlib import Path
from typing import Union, Optional, OrderedDict

from bicp_document_structure.app.workbook_container.WorkbookContainer import WorkbookContainer
from bicp_document_structure.util.Util import typeCheck, multiTypeCheck
from bicp_document_structure.workbook.WorkBook import Workbook
from bicp_document_structure.workbook.WorkbookFileInfo import WorkbookFileInfo
from bicp_document_structure.workbook.WorkbookFileInfoImp import WorkbookFileInfoImp
from bicp_document_structure.workbook.WorkbookImp import WorkbookImp


class WorkbookContainerImp(WorkbookContainer):

    def __init__(self, wbDict: OrderedDict = None):
        if wbDict is None:
            wbDict = OD()
        typeCheck(wbDict, "wbDict", OrderedDict)
        self.__wbDict = wbDict

    ### >> WorkbookContainer << ###

    def getWorkbook(self, key: WorkbookFileInfo) -> Optional[Workbook]:
        return self.getWorkbookByFileInfo(key)

    def getWorkbookByIndex(self, index: int):
        if 0 <= index < len(self.__wbDict):
            return list(self.__wbDict.items())[index][1]
        else:
            raise ValueError("Workbook at {i} does not exist".format(i=index))

    def getWorkbookByName(self, name: str):
        for k,v in self.__wbDict.items():
            if k.fileName == name:
                return v
        raise ValueError("Workbook named {n} does not exist".format(n=name))

    def getWorkbookByPath(self, path: Path):
        for k,v in self.__wbDict.items():
            if k.filePath == path:
                return v
        raise ValueError("Workbook at path {n} does not exist".format(n=str(path)))

    def getWorkbookByFileInfo(self, fileInfo: WorkbookFileInfo):
        key = fileInfo
        if key in self.__wbDict.keys():
            return self.__wbDict[key]
        else:
            raise ValueError(
                "{wbn} does not exist (file = {fd})".format(wbn=key.fileName, fd=key.filePath))

    def createNewWorkbook(self, workbookName: str):
        key = WorkbookFileInfoImp(workbookName, None)
        self.__wbDict[key] = WorkbookImp(workbookName)

    def removeWorkbook(self, indexOrKey: Union[int, WorkbookFileInfo]):
        multiTypeCheck(indexOrKey, "indexOrKey", [int, WorkbookFileInfo])
        if isinstance(indexOrKey, int):
            if 0 <= indexOrKey < len(self.__wbDict):
                k = list(self.__wbDict.items())[indexOrKey][0]
                del self.__wbDict[k]
            return
        if isinstance(indexOrKey, WorkbookFileInfo):
            if indexOrKey in self.__wbDict.keys():
                del self.__wbDict[indexOrKey]
            return

    def isEmpty(self) -> bool:
        return len(self.__wbDict) == 0

    def isNotEmpty(self) -> bool:
        return super().isNotEmpty()

    @property
    def bookCount(self):
        return len(self.__wbDict)
