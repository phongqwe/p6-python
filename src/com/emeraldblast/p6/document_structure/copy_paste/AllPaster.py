from com.emeraldblast.p6.document_structure.communication.event.data_structure.range_event.RangeCopy import RangeCopy
from com.emeraldblast.p6.document_structure.copy_paste.Paster import Paster
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.emeraldblast.p6.document_structure.util.result.Result import Result


class AllPaster(Paster):

    def __init__(self, protoPaster: Paster, textPaster: Paster, dfPaster: Paster):
        self.dfPaster = dfPaster
        self.textPaster = textPaster
        self.protoPaster = protoPaster

    def pasteRange(self) -> Result[RangeCopy, ErrorReport]:
        pass
