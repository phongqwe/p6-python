from bicp_document_structure.common.ToJsonStr import ToJson
from bicp_document_structure.workbook.WorkBook import Workbook
from bicp_document_structure.worksheet.Worksheet import Worksheet


class WorksheetEventData(ToJson):

    def __init__(self, workbook: Workbook, worksheet: Worksheet):
        self.workbook = workbook
        self.worksheet = worksheet

    def toJsonDict(self) -> dict:
        return {
            "workbook": self.workbook.name,
            "worksheet":self.worksheet.name,
        }
