from collections import OrderedDict
from pathlib import Path

from bicp_document_structure.workbook import WorkbookJson
from bicp_document_structure.workbook.WorkBook import Workbook
from bicp_document_structure.workbook.WorkbookImp import WorkbookImp
from bicp_document_structure.worksheet.Worksheets import Worksheets


class Workbooks:
    @staticmethod
    def wbFromJson(wbJson: WorkbookJson, filePath: Path) -> Workbook:
        sheetDict = OrderedDict()
        for sheetJson in wbJson.worksheets:
            sheet = Worksheets.wsFromJson(sheetJson)
            sheetDict[sheet.name]=sheet
        wb = WorkbookImp(
            name=filePath.name,
            path=filePath,
            sheetDict=sheetDict
        )
        return wb




