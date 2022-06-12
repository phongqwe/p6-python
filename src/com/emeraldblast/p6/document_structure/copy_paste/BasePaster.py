from abc import ABC

from com.emeraldblast.p6.document_structure.copy_paste.CopyErrors import CopyErrors

from com.emeraldblast.p6.document_structure.communication.event.data_structure.range_event.RangeCopy import RangeCopy
from com.emeraldblast.p6.document_structure.copy_paste.Paster import Paster
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.emeraldblast.p6.document_structure.util.result.Err import Err
from com.emeraldblast.p6.document_structure.util.result.Result import Result


class BasePaster(Paster,ABC):

    def pasteRange(self) -> Result[RangeCopy, ErrorReport]:
        try:
            return self.doPaste()
        except Exception as e:
            return Err(CopyErrors.UnableToPasteRange.report(e))

    def doPaste(self) -> Result[RangeCopy, ErrorReport]:
        raise NotImplementedError()
