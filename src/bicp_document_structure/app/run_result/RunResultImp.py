from bicp_document_structure.app.run_result.RunResult import RunResult
from bicp_document_structure.app.run_result.RunResultJson import RunResultJson
from bicp_document_structure.cell.address.CellAddress import CellAddress
from bicp_document_structure.workbook.WorkbookKey import WorkbookKey


class RunResultImp(RunResult):

    def __init__(self):
        self.__mutatedCellDict = {}
        self.__deletedCellDict = {}

    def addMutatedCell(self,workbookKey: WorkbookKey, worksheetName: str, cell: CellAddress):
        pass
    def addDeletedCell(self, workbookKey: WorkbookKey, worksheetName: str, cell: CellAddress):
        pass
    def clearResult(self):
        self.__mutatedCellDict = {}
        self.__deletedCellDict = {}

    def toJson(self) -> RunResultJson:
        mutatedCellJson = []
        deletedCellJson = []
        for cell in self.__mutatedCellDict:
            mutatedCellJson.append(cell.toJson())

        for cell in self.__deletedCellDict:
            deletedCellJson.append(cell.toJson())

        return RunResultJson(mutatedCellJson,deletedCellJson)


