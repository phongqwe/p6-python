from bicp_document_structure.cell.Cells import Cells
from bicp_document_structure.worksheet.Worksheet import Worksheet
from bicp_document_structure.worksheet.WorksheetImp import WorksheetImp
from bicp_document_structure.worksheet.WorksheetJson import WorksheetJson


class Worksheets:
    @staticmethod
    def wsFromJson(worksheetJson: WorksheetJson) -> Worksheet:
        """create a Worksheet object from a WorksheetJson object"""
        ws = WorksheetImp(name=worksheetJson.name)
        for cellJson in worksheetJson:
            cell = Cells.cellFromJson(cellJson)
            ws.addCell(cell)
        return ws
