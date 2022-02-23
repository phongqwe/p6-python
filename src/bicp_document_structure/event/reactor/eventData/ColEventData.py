from bicp_document_structure.column.Column import Column
from bicp_document_structure.common.ToJsonStr import ToJson
from bicp_document_structure.event.P6Event import P6Event
from bicp_document_structure.workbook.WorkBook import Workbook
from bicp_document_structure.worksheet.Worksheet import Worksheet


class ColEventData(ToJson):

    def __init__(self, workbook: Workbook, worksheet: Worksheet, targetRange: Column,event:P6Event):
        self.col = targetRange
        self.workbook = workbook
        self.worksheet = worksheet
        self.event = event

    def toJsonDict(self) -> dict:
        return {
            "col": self.col.index,
            "workbook": self.workbook.name,
            "worksheet":self.worksheet.name,
        }
