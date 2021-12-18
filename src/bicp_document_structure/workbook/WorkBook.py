from typing import Optional, Union

from bicp_document_structure.sheet.Worksheet import Worksheet


class Workbook:

    def getSheetByName(self,name:str)->Optional[Worksheet]:
        """
        :param name: sheet name
        :return: the sheet having that name or None if no such sheet exists
        """
        pass

    def getSheetByIndex(self,index:int)->Optional[Worksheet]:
        """
        :param index: index of a sheet
        :return: the sheet at that index, or None if no such sheet exists
        """
        pass

    def getSheet(self,nameOrIndex:Union[str,int])->Optional[Worksheet]:
        """
        get a sheet either by name or index
        :param nameOrIndex: name or index
        :return: the sheet at that index/name, or None if no such sheet exists
        """
        pass

    def isEmpty(self)->bool:
        """
        :return: true if this workbook contains zero sheet
        """
        pass

    @property
    def sheetCount(self)->int:
        pass

    @property
    def name(self)->str:
        pass

    @name.setter
    def name(self,newName:str):
        pass

    def createNewSheet(self, newSheetName:str)->Worksheet:
        """
        add a new empty sheet to this workbook
        :param newSheetName: name of the new sheet
        :return the new worksheet
        :raise ValueError if the newSheetName already exists
        """
        pass

    def removeSheetByName(self,sheetName:str)->Optional[Worksheet]:
        """ remove sheet by name. If the target sheet does not exist, simply return"""
        pass

    def removeSheetByIndex(self,index:int)->Optional[Worksheet]:
        """ remove sheet by index. If the target sheet does not exist, simply return"""
        pass

    def removeSheet(self,nameOrIndex:Union[str,int])->Optional[Worksheet]:
        """ remove sheet by either index or name. If the target sheet does not exist, simply return"""
        pass