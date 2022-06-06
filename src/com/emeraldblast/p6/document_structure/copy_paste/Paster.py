from abc import ABC

from com.emeraldblast.p6.document_structure.communication.event.data_structure.range_event.RangeCopy import RangeCopy
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.emeraldblast.p6.document_structure.util.result.Result import Result


class Paster(ABC):
    def pasteRange(self)->Result[RangeCopy,ErrorReport]:
        raise NotImplementedError()
    def pasteText(self)->Result[None,ErrorReport]:
        raise NotImplementedError()