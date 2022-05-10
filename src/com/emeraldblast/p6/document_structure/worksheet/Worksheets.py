from com.emeraldblast.p6.proto.DocProtos_pb2 import WorksheetProto

from com.emeraldblast.p6.document_structure.cell.Cells import Cells
from com.emeraldblast.p6.document_structure.workbook.WorkBook import Workbook
from com.emeraldblast.p6.document_structure.worksheet.Worksheet import Worksheet
from com.emeraldblast.p6.document_structure.worksheet.WorksheetImp import WorksheetImp
from com.emeraldblast.p6.document_structure.worksheet.WorksheetJson import WorksheetJson


class Worksheets:
    @staticmethod
    def fromProto(wsProto:WorksheetProto, workbook:Workbook):
        ws = WorksheetImp(name = wsProto.name, workbook = workbook)
        for cellProto in wsProto.cell:
            tmpCell = Cells.fromProto(cellProto)
            ws.addCell(tmpCell)
        return ws

    @staticmethod
    def wsFromJson(worksheetJson: WorksheetJson,workbook:Workbook) -> Worksheet:
        """create a Worksheet object from a WorksheetJson object"""
        ws = WorksheetImp(name = worksheetJson.name,workbook = workbook)
        for cellJson in worksheetJson.cells:
            cell = Cells.cellFromJson(cellJson)
            ws.addCell(cell)
        return ws
