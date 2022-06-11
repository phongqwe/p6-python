from typing import Optional, Tuple

from com.emeraldblast.p6.document_structure.cell.Cell import Cell
from com.emeraldblast.p6.document_structure.cell.address.CellAddress import CellAddress
from com.emeraldblast.p6.document_structure.copy_paste.Paster import Paster
from com.emeraldblast.p6.document_structure.formula_translator.FormulaTranslator import FormulaTranslator
from com.emeraldblast.p6.document_structure.range.Range import Range
from com.emeraldblast.p6.document_structure.range.address.RangeAddress import RangeAddress
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.emeraldblast.p6.document_structure.util.result.Result import Result
from com.emeraldblast.p6.document_structure.workbook.WorkBook import Workbook
from com.emeraldblast.p6.document_structure.worksheet.Worksheet import Worksheet
from com.emeraldblast.p6.document_structure.worksheet.WorksheetJson import WorksheetJson


class WorksheetWrapper(Worksheet):

    def __init__(self, innerWorksheet: Worksheet):
        self._innerSheet: Worksheet = innerWorksheet

    def pasteDataFrameFromClipboardRs(self, anchorCell: CellAddress) -> Result[None, ErrorReport]:
        return self.rootWorksheet.pasteDataFrameFromClipboardRs(anchorCell)

    def pasteProtoFromClipboardRs(
            self, anchorCell:
            CellAddress, paster: Paster | None = None) -> Result[None, ErrorReport]:
        return self.rootWorksheet.pasteProtoFromClipboardRs(anchorCell, paster)

    @property
    def colDict(self) -> dict[int, list[Cell]]:
        return self.rootWorksheet.colDict

    @property
    def rowDict(self) -> dict[int, list[Cell]]:
        return self.rootWorksheet.rowDict

    @property
    def maxUsedCol(self) -> int | None:
        return self.rootWorksheet.maxUsedCol

    @property
    def minUsedCol(self) -> int | None:
        return self.rootWorksheet.minUsedCol

    @property
    def maxUsedRow(self) -> int | None:
        return self.rootWorksheet.maxUsedRow

    @property
    def minUsedRow(self) -> int | None:
        return self.rootWorksheet.minUsedRow

    @property
    def usedRangeAddress(self) -> RangeAddress | None:
        return self.rootWorksheet.usedRangeAddress

    def pasteDataFrameFromClipboardRs(self, anchorCell: CellAddress) -> Result[None, ErrorReport]:
        return self.rootWorksheet.pasteDataFrameFromClipboardRs(anchorCell)

    def hasCellAtIndex(self, col: int, row: int) -> bool:
        return self.rootWorksheet.hasCellAtIndex(col, row)

    def containsAddressIndex(self, col: int, row: int) -> bool:
        return self.containsAddressIndex(col, row)

    def deleteRangeRs(self, rangeAddress: RangeAddress) -> Result[None, ErrorReport]:
        return self.rootWorksheet.deleteRangeRs(rangeAddress)

    def deleteCellRs(self, address: CellAddress | Tuple[int, int] | str) -> Result[None, ErrorReport]:
        return self.rootWorksheet.deleteCellRs(address)

    @property
    def rootWorksheet(self) -> 'Worksheet':
        return self._innerSheet.rootWorksheet

    @property
    def workbook(self) -> Workbook | None:
        return self.rootWorksheet.workbook

    @workbook.setter
    def workbook(self, newWorkbook: Workbook | None):
        self.rootWorksheet.workbook = newWorkbook

    @property
    def translator(self) -> FormulaTranslator:
        return self.rootWorksheet.translator

    @property
    def name(self) -> str:
        return self.rootWorksheet.name

    @property
    def size(self) -> int:
        return self.rootWorksheet.size

    def toJson(self) -> WorksheetJson:
        return self.rootWorksheet.toJson()

    def cell(self, address: str | CellAddress | Tuple[int, int]) -> Cell:
        return self.rootWorksheet.cell(address)

    def range(self, rangeAddress: str | RangeAddress | Tuple[CellAddress, CellAddress]) -> Range:
        return self.rootWorksheet.range(rangeAddress)

    def addCell(self, cell: Cell):
        self.rootWorksheet.addCell(cell)

    def getOrMakeCell(self, address: CellAddress) -> Cell:
        return self.rootWorksheet.getOrMakeCell(address)

    def hasCellAt(self, address: CellAddress) -> bool:
        return self.rootWorksheet.hasCellAt(address)

    def getCell(self, address: CellAddress) -> Optional[Cell]:
        return self.rootWorksheet.getCell(address)

    def isEmpty(self) -> bool:
        return self.rootWorksheet.isEmpty()

    def containsAddress(self, address: CellAddress) -> bool:
        return self.rootWorksheet.containsAddress(address)

    @property
    def cells(self) -> list[Cell]:
        return self.rootWorksheet.cells

    @property
    def rangeAddress(self) -> RangeAddress:
        return self.rootWorksheet.rangeAddress

    def toJsonDict(self) -> dict:
        return self.rootWorksheet.toJsonDict()

    def reportJsonStr(self) -> str:
        return self.rootWorksheet.reportJsonStr()

    def isSameRangeAddress(self, other):
        return self.rootWorksheet.isSameRangeAddress(other)

    def reRun(self, refreshScript: bool = False):
        self.rootWorksheet.reRun(refreshScript)

    @property
    def innerSheet(self):
        return self.rootWorksheet

    def internalRename(self, newName: str):
        self.rootWorksheet.internalRename(newName)

    def renameRs(self, newName: str) -> Result[None, ErrorReport]:
        return self.rootWorksheet.renameRs(newName)
