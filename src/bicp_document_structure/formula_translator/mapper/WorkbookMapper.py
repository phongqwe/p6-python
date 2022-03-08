class WorkbookMapper:
    __instance = None
    @staticmethod
    def instance():
        if WorkbookMapper.__instance is None:
            WorkbookMapper.__instance = WorkbookMapper()
        return WorkbookMapper.__instance

    def getSheet(self,sheetName: str)->str:
        return "getSheet(\"{sn}\")".format(sn=sheetName)