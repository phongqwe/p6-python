from com.github.xadkile.bicp.doc.data_structure.sheet.Sheet import Sheet


class Workbook:
    def __init__(self,sheetDict):
        if type(sheetDict) is dict:
            self.__sheetDict = sheetDict
        else:
            raise ValueError("sheetDict must be a dict")

    @staticmethod
    def empty():
        return Workbook(dict())

    def addSheet(self, newSheetName):
        """
        add a new empty sheet to this workbook
        :param newSheetName: name of the new sheet
        """
        self.__sheetDict[newSheetName] = Sheet.empty()

    def removeSheet(self,sheetName):
        del self.__sheetDict[sheetName]

