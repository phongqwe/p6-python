class PythonMapper:

    def __init__(self):
        self.z=1

    def rangeAddress(self,rangeAddress: str)->str:
        return "\"@{ra}\"".format(ra=rangeAddress)

    def getSheet(self,sheetName: str)->str:
        return "getSheet(\"{sn}\")".format(sn=sheetName)

    def getRange(self,rangeAddress: str)->str:
        return "getRange({ra})".format(ra=rangeAddress)

    def getCell(self,cellAddress: str)->str:
        return "cell({ca})".format(ca=cellAddress)

    def getWorkbook(self,workbookName: str)->str:
        return "getWorkbook(\"{wbn}\")".format(wbn=workbookName)

    def getWorkbook(self,index: int)->str:
        return "getWorkbook({i})".format(i=str(index))