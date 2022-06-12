from abc import ABC

from com.emeraldblast.p6.document_structure.cell.address.CellAddress import CellAddress
from com.emeraldblast.p6.document_structure.communication.event.data_structure.range_event.RangeCopy import RangeCopy
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.emeraldblast.p6.document_structure.util.result.Result import Result


class Paster(ABC):
    def pasteRange(self,anchorCell: CellAddress)->Result[RangeCopy,ErrorReport]:
        """read the clipboard and convert the data into a RangeCopy obj"""
        raise NotImplementedError()