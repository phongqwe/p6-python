from typing import Any, TypeVar, Generic

from bicp_document_structure.message.event.P6Event import P6Event
from bicp_document_structure.message.event.reactor.eventData.WithWorkbookData import WithWorkbookData
from bicp_document_structure.util.ToJson import ToJson
from bicp_document_structure.workbook.WorkBook import Workbook
from bicp_document_structure.worksheet.Worksheet import Worksheet

D = TypeVar("D")
class WorksheetEventData(ToJson, WithWorkbookData,Generic[D]):

    def __init__(self,
                 workbook: Workbook,
                 worksheet: Worksheet,
                 event: P6Event,
                 data: D = None,
                 isError: bool = False):
        self._workbook = workbook
        self.worksheet = worksheet
        self.event = event
        self.data: D = data
        self.isError = isError

    @property
    def workbook(self):
        return self._workbook

    def toJsonDict(self) -> dict:
        return {
            "workbook": self.workbook.name,
            "worksheet": self.worksheet.name,
            "supportData": self.data.__dict__()
        }
