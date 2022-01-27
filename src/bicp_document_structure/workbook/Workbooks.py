from collections import OrderedDict
from pathlib import Path
from typing import Union

from bicp_document_structure.file.P6Files import P6Files
from bicp_document_structure.workbook import WorkbookJson
from bicp_document_structure.workbook.WorkBook import Workbook
from bicp_document_structure.workbook.WorkbookImp import WorkbookImp
from bicp_document_structure.worksheet.Worksheets import Worksheets


class Workbooks:
    @staticmethod
    def wbFromJson(wbJson: WorkbookJson, filePath: Union[Path, None] = None) -> Workbook:
        """NOTE: this function use the file name as the name for the newly created Workbook"""
        path = filePath
        if filePath is None:
            if wbJson.path is None:
                path = P6Files.defaultPath
            else:
                path = Path(wbJson.path)

        sheetDict = OrderedDict()
        for sheetJson in wbJson.worksheets:
            sheet = Worksheets.wsFromJson(sheetJson)
            sheetDict[sheet.name] = sheet
        wb = WorkbookImp(
            name=path.name,
            path=path,
            sheetDict=sheetDict
        )
        return wb
