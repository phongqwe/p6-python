class WorkbookMapper:
    __instance = None
    @staticmethod
    def instance():
        if WorkbookMapper.__instance is None:
            WorkbookMapper.__instance = WorkbookMapper()
        return WorkbookMapper.__instance

    def getWorksheet(self,sheetName: str)->str:
        return "getWorksheet(\"{sn}\")".format(sn=sheetName)