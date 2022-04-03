from typing import TypeVar, Generic

from bicp_document_structure.communication.event.P6Event import P6Event
from bicp_document_structure.communication.internal_reactor.eventData.WithWorkbookData import WithWorkbookData
from bicp_document_structure.util.ToJson import ToJson
from bicp_document_structure.workbook.WorkBook import Workbook
from bicp_document_structure.worksheet.Worksheet import Worksheet

D = TypeVar("D")
class WorksheetEventData(ToJson, WithWorkbookData,Generic[D]):

    def __init__(self,
                 workbook: Workbook=None,
                 worksheet: Worksheet=None,
                 event: P6Event=None,
                 data: D = None):
        self._workbook = workbook
        self.worksheet = worksheet
        self.event = event
        self.data: D = data

    @property
    def workbook(self):
        return self._workbook

    @workbook.setter
    def workbook(self,wb):
        self._workbook = wb

    def toJsonDict(self) -> dict:
        return {
            "workbook": self.workbook.name,
            "worksheet": self.worksheet.name,
            "supportData": self.data.__dict__()
        }
