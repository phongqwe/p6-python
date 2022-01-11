from abc import ABC

from bicp_document_structure.cell.address.CellAddress import CellAddress
from bicp_document_structure.mutation.CellMutationEvent import CellMutationEvent
from bicp_document_structure.workbook.WorkbookKey import WorkbookKey


class CellMutationEventHandler(ABC):
    def onCellMutation(self,workbookKey: WorkbookKey,
                       worksheetName: str,
                       cellAddress: CellAddress,
                       mutationEvent:CellMutationEvent):
        raise NotImplementedError()