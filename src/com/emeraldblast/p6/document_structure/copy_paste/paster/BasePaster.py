from abc import ABC

from com.emeraldblast.p6.document_structure.cell.address.CellAddress import CellAddress
from com.emeraldblast.p6.document_structure.copy_paste.CopyPasteErrors import CopyPasteErrors

from com.emeraldblast.p6.document_structure.communication.event.data_structure.range_event.RangeCopy import RangeCopy
from com.emeraldblast.p6.document_structure.copy_paste.paster.Paster import Paster
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.emeraldblast.p6.document_structure.util.result.Err import Err
from com.emeraldblast.p6.document_structure.util.result.Result import Result


class BasePaster(Paster,ABC):

    def pasteRange(self,anchorCell: CellAddress) -> Result[RangeCopy, ErrorReport]:
        try:
            return self.doPaste(anchorCell)
        except Exception as e:
            return Err(CopyPasteErrors.UnableToPasteRange.report(e))

    def doPaste(self,anchorCell: CellAddress) -> Result[RangeCopy, ErrorReport]:
        raise NotImplementedError()
