from com.emeraldblast.p6.document_structure.cell.address.CellAddress import CellAddress
from com.emeraldblast.p6.document_structure.communication.event.data_structure.range_event.RangeCopy import RangeCopy
from com.emeraldblast.p6.document_structure.copy_paste.paster.BasePaster import BasePaster
from com.emeraldblast.p6.document_structure.copy_paste.paster.Paster import Paster
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.emeraldblast.p6.document_structure.util.result.Result import Result


class UnifiedPaster(BasePaster):

    def __init__(self, protoPaster: Paster, textPaster: Paster, dfPaster: Paster):
        self.dfPaster = dfPaster
        self.textPaster = textPaster
        self.protoPaster = protoPaster

    def doPaste(self, anchorCell: CellAddress) -> Result[RangeCopy, ErrorReport]:
        protoRs = self.protoPaster.pasteRange(anchorCell)
        if protoRs.isOk():
            return protoRs
        else:
            dfRs = self.dfPaster.pasteRange(anchorCell)
            if dfRs.isOk():
                return dfRs
            else:
                textRs = self.textPaster.pasteRange(anchorCell)
                return textRs


