from bicp_document_structure.message.event.P6Event import P6Event
from bicp_document_structure.message.event.reactor.eventData.WithWorkbookData import WithWorkbookData
from bicp_document_structure.util.ToJson import ToJson
from bicp_document_structure.workbook.WorkBook import Workbook


class WorkbookEventData(ToJson,WithWorkbookData):

    def __init__(self, workbook: Workbook,event:P6Event):
        self._workbook = workbook
        self.event = event

    @property
    def workbook(self):
        return self._workbook

    def toJsonDict(self) -> dict:
        return {
            "workbook": self.workbook.name,
        }
