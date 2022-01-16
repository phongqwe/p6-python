from bicp_document_structure.app.mutation_handler.CellMutatorEventHandler import CellMutationEventHandler
from bicp_document_structure.app.run_result.RunResult import RunResult
from bicp_document_structure.cell.Cell import Cell
from bicp_document_structure.mutation.CellMutationEvent import CellMutationEvent
from bicp_document_structure.workbook.WorkbookKey import WorkbookKey


class RunResultCMEHandler(CellMutationEventHandler):
    def __init__(self, runResult: RunResult):
        self.__runResult: RunResult = runResult

    def onCellMutation(self, workbookKey: WorkbookKey, 
                       worksheetName: str, 
                       cell: Cell,
                       mutationEvent: CellMutationEvent):
        runResult = self.__runResult
        if mutationEvent == CellMutationEvent.DELETED:
            if runResult.containCellInMutated(workbookKey, worksheetName, cell.address):
                runResult.removeMutatedCell(workbookKey, worksheetName, cell.address)
            runResult.addDeletedCell(workbookKey, worksheetName, cell.address)
        elif mutationEvent == CellMutationEvent.NEW_VALUE or mutationEvent == CellMutationEvent.NEW_SCRIPT:
            if runResult.containCellInDeleted(workbookKey, worksheetName, cell.address):
                runResult.removeDeletedCell(workbookKey, worksheetName, cell.address)
            runResult.addMutatedCell(workbookKey, worksheetName, cell.address)