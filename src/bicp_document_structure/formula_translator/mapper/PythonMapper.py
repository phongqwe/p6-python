from bicp_document_structure.workbook.key.WorkbookKey import WorkbookKey


class PythonMapper:
    __instance = None

    @staticmethod
    def instance():
        if PythonMapper.__instance is None:
            PythonMapper.__instance = PythonMapper()
        return PythonMapper.__instance

    def formatRangeAddress(self, rangeAddress: str)->str:
        return "\"@{ra}\"".format(ra=rangeAddress)

    def getSheet(self,sheetName: str)->str:
        return "getSheet(\"{sn}\")".format(sn=sheetName)

    def getRange(self,rangeAddress: str)->str:
        return "getRange({ra})".format(ra=rangeAddress)

    def getCell(self,cellAddress: str)->str:
        return "cell({ca})".format(ca=cellAddress)
    def getActiveWorkbook(self):
        return "getActiveWorkbook()"
    def getWorkbook(self, workbookNameOrKeyOrIndex: str | int | WorkbookKey)->str:
        if isinstance(workbookNameOrKeyOrIndex, str):
            return "getWorkbook(\"{wbn}\")".format(wbn=workbookNameOrKeyOrIndex)
        elif isinstance(workbookNameOrKeyOrIndex,int):
            return f"getWorkbook({workbookNameOrKeyOrIndex})"
        else:
            name = workbookNameOrKeyOrIndex.fileName
            path = None
            if workbookNameOrKeyOrIndex.filePath is not None:
                path = f'"{str(workbookNameOrKeyOrIndex.filePath)}"'
            return f'getWorkbook(WorkbookKeys.fromNameAndPath("{name}",{path}))'
