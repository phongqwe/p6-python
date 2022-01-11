from bicp_document_structure.app.mutation_handler.CellMutatorEventHandler import CellMutationEventHandler
from bicp_document_structure.app.run_result.RunResult import RunResult
from bicp_document_structure.cell.address.CellAddress import CellAddress
from bicp_document_structure.mutation.CellMutationEvent import CellMutationEvent
from bicp_document_structure.workbook.WorkbookKey import WorkbookKey


class CellMutationEventHandlerImp(CellMutationEventHandler):
    def __init__(self, runResult: RunResult):
        self.__runResult: RunResult = runResult

    def onCellMutation(self, workbookKey: WorkbookKey, 
                       worksheetName: str, 
                       cellAddress: CellAddress,
                       mutationEvent: CellMutationEvent):
        runResult = self.__runResult
        if mutationEvent == CellMutationEvent.DELETED:
            if runResult.containCellInMutated(workbookKey, worksheetName, cellAddress):
                runResult.removeMutatedCell(workbookKey, worksheetName, cellAddress)
            runResult.addDeletedCell(workbookKey, worksheetName, cellAddress)
        elif mutationEvent == CellMutationEvent.NEW_VALUE or mutationEvent == CellMutationEvent.NEW_SCRIPT:
            if runResult.containCellInDeleted(workbookKey, worksheetName, cellAddress):
                runResult.removeDeletedCell(workbookKey, worksheetName, cellAddress)
            runResult.addMutatedCell(workbookKey, worksheetName, cellAddress)