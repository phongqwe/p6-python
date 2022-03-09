class WorksheetMapper:
    __instance = None

    @staticmethod
    def instance():
        if WorksheetMapper.__instance is None:
            WorksheetMapper.__instance = WorksheetMapper()
        return WorksheetMapper.__instance


    def getRange(self,rangeAddress: str)->str:
        return "range({ra})".format(ra=rangeAddress)

    def getCell(self,cellAddress: str)->str:
        return "cell({ca})".format(ca=cellAddress)