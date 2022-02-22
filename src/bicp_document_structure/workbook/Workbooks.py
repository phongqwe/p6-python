from pathlib import Path
from typing import Union, Callable

from bicp_document_structure.cell.Cell import Cell
from bicp_document_structure.cell.Cells import Cells
from bicp_document_structure.event.P6Event import P6Event
from bicp_document_structure.file.P6Files import P6Files
from bicp_document_structure.workbook import WorkbookJson
from bicp_document_structure.workbook.EventWorkbook import EventWorkbook
from bicp_document_structure.workbook.WorkBook import Workbook
from bicp_document_structure.workbook.WorkbookImp import WorkbookImp
from bicp_document_structure.worksheet.Worksheet import Worksheet


class Workbooks:
    @staticmethod
    def eventWBFromJson(wbJson: WorkbookJson,
                        filePath: Union[Path, None] = None,
                        onCellChange: Callable[[Workbook, Worksheet, Cell, P6Event], None] = None,
                        ) -> Workbook:
        """NOTE: this function use the file name as the name for the newly created Workbook"""
        wb = EventWorkbook(Workbooks.wbFromJson(wbJson, filePath), onCellChange)
        return wb

    @staticmethod
    def wbFromJson(wbJson: WorkbookJson, filePath: Union[Path, None] = None) -> Workbook:
        path = filePath
        if filePath is None:
            if wbJson.path is None:
                path = P6Files.defaultPath
            else:
                path = Path(wbJson.path)

        wb = WorkbookImp(
            name = path.name,
            path = path,
        )

        for sheetJson in wbJson.worksheets:
            sheet: Worksheet = wb.createNewWorksheet(sheetJson.name)
            for cellJson in sheetJson.cells:
                dummyCell = Cells.cellFromJson(cellJson)
                realCell = sheet.cell(dummyCell.address)
                realCell.copyFrom(dummyCell)
        return wb
