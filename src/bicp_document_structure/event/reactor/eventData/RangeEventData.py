from bicp_document_structure.common.ToJsonStr import ToJson
from bicp_document_structure.range.Range import Range
from bicp_document_structure.workbook.WorkBook import Workbook
from bicp_document_structure.worksheet.Worksheet import Worksheet


class RangeEventData(ToJson):

    def __init__(self, workbook: Workbook, worksheet: Worksheet, targetRange: Range):
        self.range = targetRange
        self.workbook = workbook
        self.worksheet = worksheet

    def toJsonDict(self) -> dict:
        return {
            "rangeAddress": self.range.rangeAddress.label,
            "workbook": self.workbook.name,
            "worksheet":self.worksheet.name,
        }
