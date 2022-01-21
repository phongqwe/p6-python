from bicp_document_structure.app.run_result.RunResult import RunResult
from bicp_document_structure.app.run_result.RunResultJson import RunResultJson
from bicp_document_structure.app.run_result.SingleResultDict import SingleResultDict
from bicp_document_structure.app.workbook_container.WorkbookContainer import WorkbookContainer
from bicp_document_structure.cell.address.CellAddress import CellAddress
from bicp_document_structure.workbook.WorkbookKey import WorkbookKey


class RunResultImp(RunResult):

    def __init__(self):
        self.__mutatedCellDict = SingleResultDict()
        self.__deletedCellDict = SingleResultDict()

    def addMutatedCell(self, workbookKey: WorkbookKey, worksheetName: str, cellAddress: CellAddress):
        self.__mutatedCellDict.add(workbookKey, worksheetName, cellAddress)

    def addDeletedCell(self, workbookKey: WorkbookKey, worksheetName: str, cellAddress: CellAddress):
        self.__deletedCellDict.add(workbookKey, worksheetName, cellAddress)

    def removeDeletedCell(self, workbookKey: WorkbookKey, worksheetName: str, cellAddress: CellAddress):
        self.__deletedCellDict.remove(workbookKey, worksheetName, cellAddress)

    def removeMutatedCell(self, workbookKey: WorkbookKey, worksheetName: str, cellAddress: CellAddress):
        self.__mutatedCellDict.remove(workbookKey, worksheetName, cellAddress)

    def containCellInDeleted(self,
                             workbookKey: WorkbookKey,
                             worksheetName: str,
                             cellAddress: CellAddress):
        return self.__deletedCellDict.checkContain(workbookKey,worksheetName,cellAddress)

    def containCellInMutated(self,
                             workbookKey: WorkbookKey,
                             worksheetName: str,
                             cellAddress: CellAddress):
        return self.__mutatedCellDict.checkContain( workbookKey, worksheetName, cellAddress)
    

    def clearResult(self):
        self.__mutatedCellDict.clear()
        self.__deletedCellDict.clear()

    def toJson(self,workbookContainer:WorkbookContainer) -> RunResultJson:
        mutatedCellJson = []
        deletedCellJson = []
        return RunResultJson(mutatedCellJson, deletedCellJson)
