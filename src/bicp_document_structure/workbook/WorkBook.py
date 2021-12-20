from abc import ABC
from typing import Optional, Union

from bicp_document_structure.workbook.WorkbookFileInfo import WorkbookFileInfo
from bicp_document_structure.worksheet.Worksheet import Worksheet


class Workbook(ABC):

    @property
    def fileInfo(self)->WorkbookFileInfo:
        raise NotImplementedError()
    @property
    def activeSheet(self)->Optional[Worksheet]:
        raise NotImplementedError()

    def setActiveSheet(self, indexOrName:Union[int, str]):
        raise NotImplementedError()

    def getSheetByName(self,name:str)->Optional[Worksheet]:
        """
        :param name: sheet name
        :return: the sheet having that name or None if no such sheet exists
        """
        raise NotImplementedError()

    def getSheetByIndex(self,index:int)->Optional[Worksheet]:
        """
        :param index: index of a sheet
        :return: the sheet at that index, or None if no such sheet exists
        """
        raise NotImplementedError()

    def getSheet(self,nameOrIndex:Union[str,int])->Optional[Worksheet]:
        """
        get a sheet either by name or index
        :param nameOrIndex: name or index
        :return: the sheet at that index/name, or None if no such sheet exists
        """
        raise NotImplementedError()

    def isEmpty(self)->bool:
        """
        :return: true if this workbook contains zero sheet
        """
        raise NotImplementedError()

    @property
    def sheetCount(self)->int:
        raise NotImplementedError()

    @property
    def name(self)->str:
        raise NotImplementedError()

    @name.setter
    def name(self,newName:str):
        raise NotImplementedError()

    def createNewSheet(self, newSheetName:str)->Worksheet:
        """
        add a new empty sheet to this workbook
        :param newSheetName: name of the new sheet
        :return the new worksheet
        :raise ValueError if the newSheetName already exists
        """
        raise NotImplementedError()

    def removeSheetByName(self,sheetName:str)->Optional[Worksheet]:
        """ remove sheet by name. If the target sheet does not exist, simply return"""
        raise NotImplementedError()

    def removeSheetByIndex(self,index:int)->Optional[Worksheet]:
        """ remove sheet by index. If the target sheet does not exist, simply return"""
        raise NotImplementedError()

    def removeSheet(self,nameOrIndex:Union[str,int])->Optional[Worksheet]:
        """ remove sheet by either index or name. If the target sheet does not exist, simply return"""
        raise NotImplementedError()