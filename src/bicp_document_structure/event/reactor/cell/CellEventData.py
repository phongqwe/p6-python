from bicp_document_structure.cell.Cell import Cell
from bicp_document_structure.workbook.WorkBook import Workbook
from bicp_document_structure.worksheet.Worksheet import Worksheet


class CellEventData:
    def __init__(self, workbook: Workbook, worksheet: Worksheet, cell: Cell):
        self.cell = cell
        self.worksheet = worksheet
        self.workbook = workbook
