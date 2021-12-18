from typing import Optional, Union

from bicp_document_structure.workbook.WorkBook import Workbook


class App:

    @property
    def activeWorkbook(self)->Optional[Workbook]:
        pass

    def getWorkbookByIndex(self,index:int)->Optional[Workbook]:
        pass

    def hasNoWorkbook(self)->bool:
        pass

    def setActiveWorkbook(self, indexOrName:Union[int,str]):
        pass

    def createNewWorkBook(self,name:str):
        pass

    def saveWorkbook(self,nameOrIndex:Union[int,str], filePath:str):
        pass

    def loadWorkbook(self,filePath:str)->bool:
        pass