from com.emeraldblast.p6.document_structure.util.ToProto import ToProto

from com.emeraldblast.p6.document_structure.communication.event.P6Event import P6Event
from com.emeraldblast.p6.document_structure.range.Range import Range
from com.emeraldblast.p6.document_structure.workbook.WorkBook import Workbook
from com.emeraldblast.p6.document_structure.worksheet.Worksheet import Worksheet


class RangeEventData:

    def __init__(self,
                 workbook: Workbook = None,
                 worksheet: Worksheet = None,
                 targetRange: Range=None,
                 event: P6Event = None,
                 isError: bool = False,
                 data: ToProto = None):
        self.range = targetRange
        self.workbook = workbook
        self.worksheet = worksheet
        self.event = event
        self.isError = isError
        self.data = data
