from com.emeraldblast.p6.document_structure.cell.Cells import Cells
from com.emeraldblast.p6.document_structure.workbook.WorkBook import Workbook
from com.emeraldblast.p6.document_structure.worksheet.Worksheet import Worksheet
from com.emeraldblast.p6.document_structure.worksheet.WorksheetImp import WorksheetImp
from com.emeraldblast.p6.document_structure.worksheet.WorksheetJson import WorksheetJson


class Worksheets:
    @staticmethod
    def wsFromJson(worksheetJson: WorksheetJson,workbook:Workbook) -> Worksheet:
        """create a Worksheet object from a WorksheetJson object"""
        ws = WorksheetImp(name = worksheetJson.name,workbook = workbook)
        for cellJson in worksheetJson.cells:
            cell = Cells.cellFromJson(cellJson)
            ws.addCell(cell)
        return ws
