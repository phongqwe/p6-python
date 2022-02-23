from bicp_document_structure.common.ToJsonStr import ToJson
from bicp_document_structure.event.P6Event import P6Event
from bicp_document_structure.workbook.WorkBook import Workbook


class WorkbookEventData(ToJson):

    def __init__(self, workbook: Workbook,event:P6Event):
        self.workbook = workbook
        self.event = event

    def toJsonDict(self) -> dict:
        return {
            "workbook": self.workbook.name,
        }
