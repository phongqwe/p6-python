from abc import ABC

from bicp_document_structure.cell.Cell import Cell
from bicp_document_structure.mutation.CellMutationEvent import CellMutationEvent
from bicp_document_structure.workbook.WorkbookKey import WorkbookKey


class CellMutationEventHandler(ABC):
    def onCellMutation(self,workbookKey: WorkbookKey,
                       worksheetName: str,
                       cell: Cell,
                       mutationEvent:CellMutationEvent):
        raise NotImplementedError()