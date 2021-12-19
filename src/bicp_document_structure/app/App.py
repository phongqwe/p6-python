from typing import Optional, Union

from bicp_document_structure.workbook.WorkBook import Workbook


class App:

    @property
    def activeWorkbook(self)->Optional[Workbook]:
        raise NotImplementedError()

    def getWorkbookByIndex(self,index:int)->Optional[Workbook]:
        raise NotImplementedError()

    def hasNoWorkbook(self)->bool:
        raise NotImplementedError()

    def setActiveWorkbook(self, indexOrName:Union[int,str]):
        raise NotImplementedError()

    def createNewWorkBook(self,name:str):
        raise NotImplementedError()

    def saveWorkbook(self,nameOrIndex:Union[int,str], filePath:str):
        raise NotImplementedError()

    def loadWorkbook(self,filePath:str)->bool:
        raise NotImplementedError()