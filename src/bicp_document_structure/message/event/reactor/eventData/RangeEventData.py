from bicp_document_structure.message.event.P6Event import P6Event
from bicp_document_structure.message.event.reactor.eventData.WithWorkbookData import WithWorkbookData
from bicp_document_structure.range.Range import Range
from bicp_document_structure.util.ToJson import ToJson
from bicp_document_structure.workbook.WorkBook import Workbook
from bicp_document_structure.worksheet.Worksheet import Worksheet


class RangeEventData(ToJson,WithWorkbookData):

    def __init__(self, workbook: Workbook, worksheet: Worksheet, targetRange: Range,event:P6Event):
        self.range = targetRange
        self._workbook = workbook
        self.worksheet = worksheet
        self.event = event

    @property
    def workbook(self):
        return self._workbook

    def toJsonDict(self) -> dict:
        return {
            "rangeAddress": self.range.rangeAddress.label,
            "workbook": self.workbook.name,
            "worksheet":self.worksheet.name,
        }