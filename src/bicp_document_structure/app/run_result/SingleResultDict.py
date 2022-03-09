from typing import Union

from bicp_document_structure.cell.address.CellAddress import CellAddress
from bicp_document_structure.workbook.key.WorkbookKey import WorkbookKey


class SingleResultDict:
    def __init__(self, mDict: Union[dict, None] = None):
        if mDict is None:
            mDict = {}
        self.__dict = mDict

    def add(self, workbookKey: WorkbookKey, worksheetName: str, cellAddress: CellAddress):
        targetDict = self.__dict
        if workbookKey not in targetDict.keys():
            targetDict[workbookKey] = {}
        wbDict = targetDict[workbookKey]
        if worksheetName not in wbDict:
            wbDict[worksheetName] = {}
        wsDict = wbDict[worksheetName]
        wsDict[cellAddress] = cellAddress

    def remove(self, workbookKey: WorkbookKey, worksheetName: str, cellAddress: CellAddress):
        if SingleResultDict._checkContain(self.__dict, workbookKey, worksheetName, cellAddress):
            del self.__dict[workbookKey][worksheetName][cellAddress]
            if len(self.__dict[workbookKey][worksheetName]) == 0:
                del self.__dict[workbookKey][worksheetName]
            if len(self.__dict[workbookKey]) == 0:
                del self.__dict[workbookKey]

    def checkContain(self, workbookKey: WorkbookKey, worksheetName: str, cellAddress: CellAddress):
        return SingleResultDict._checkContain(self.__dict, workbookKey, worksheetName, cellAddress)

    @staticmethod
    def _checkContain(targetDict, workbookKey: WorkbookKey, worksheetName: str, cellAddress: CellAddress):
        if workbookKey in targetDict.keys():
            wbDict = targetDict[workbookKey]
            if worksheetName in wbDict.keys():
                wsDict = wbDict[worksheetName]
                rt = cellAddress in wsDict.keys()
                return rt
            else:
                return False
        else:
            return False

    def clear(self):
        self.__dict = {}
