from bicp_document_structure.cell.Cell import Cell
from bicp_document_structure.common.ToJsonStr import ToJson
from bicp_document_structure.workbook.WorkBook import Workbook
from bicp_document_structure.worksheet.Worksheet import Worksheet


class CellEventData(ToJson):

    def __init__(self, workbook: Workbook, worksheet: Worksheet, cell: Cell):
        self.cell = cell
        self.worksheet = worksheet
        self.workbook = workbook

    def toJsonDict(self) -> dict:
        return {
            "workbook": {
                "name": self.workbook.name,
                "path": str(self.workbook.workbookKey.filePath)
            },
            "worksheet": self.worksheet.name,
            "cell": self.cell.toJson().toJsonDict()
        }
