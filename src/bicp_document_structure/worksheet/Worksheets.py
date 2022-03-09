from typing import Callable

from bicp_document_structure.cell.Cells import Cells
from bicp_document_structure.formula_translator.FormulaTranslator import FormulaTranslator
from bicp_document_structure.worksheet.Worksheet import Worksheet
from bicp_document_structure.worksheet.WorksheetImp2 import WorksheetImp2
from bicp_document_structure.worksheet.WorksheetJson import WorksheetJson


class Worksheets:
    @staticmethod
    def wsFromJson(worksheetJson: WorksheetJson, translatorGetter: Callable[[str], FormulaTranslator]) -> Worksheet:
        """create a Worksheet object from a WorksheetJson object"""
        ws = WorksheetImp2(name = worksheetJson.name,translatorGetter = translatorGetter)
        for cellJson in worksheetJson.cells:
            cell = Cells.cellFromJson(cellJson)
            ws.addCell(cell)
        return ws
