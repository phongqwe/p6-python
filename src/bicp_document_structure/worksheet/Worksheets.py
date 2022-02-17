from collections import Callable

from bicp_document_structure.cell.Cell import Cell
from bicp_document_structure.cell.Cells import Cells
from bicp_document_structure.event.P6Event import P6Event
from bicp_document_structure.worksheet.Worksheet import Worksheet
from bicp_document_structure.worksheet.WorksheetImp import WorksheetImp
from bicp_document_structure.worksheet.WorksheetJson import WorksheetJson


class Worksheets:
    @staticmethod
    def wsFromJson(worksheetJson: WorksheetJson,
                   onCellChange: Callable[[Worksheet, Cell, P6Event], None] = None
                   ) -> Worksheet:
        """create a Worksheet object from a WorksheetJson object"""
        ws = WorksheetImp(name = worksheetJson.name, onCellChange = onCellChange)
        for cellJson in worksheetJson:
            cell = Cells.cellFromJson(cellJson)
            ws.addCell(cell)
        return ws
