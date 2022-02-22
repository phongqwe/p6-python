from bicp_document_structure.column.Column import Column
from bicp_document_structure.common.ToJsonStr import ToJson
from bicp_document_structure.workbook.WorkBook import Workbook
from bicp_document_structure.worksheet.Worksheet import Worksheet


class ColEventData(ToJson):

    def __init__(self, workbook: Workbook, worksheet: Worksheet, targetRange: Column):
        self.col = targetRange
        self.workbook = workbook
        self.worksheet = worksheet

    def toJsonDict(self) -> dict:
        return {
            "col": self.col.index,
            "workbook": self.workbook.name,
            "worksheet":self.worksheet.name,
        }
