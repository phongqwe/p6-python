class Workbook:

    @property
    def sheetCount(self)->int:
        pass

    @property
    def name(self)->str:
        pass

    @name.setter
    def name(self,newName:str):
        pass

    def createNewSheet(self, newSheetName):
        """
        add a new empty sheet to this workbook
        :param newSheetName: name of the new sheet
        """
        pass

    def removeSheetByName(self,sheetName:str):
        pass

    def removeSheetByIndex(self,index:int):
        pass

    def removeSheet(self,nameOrIndex):
        pass