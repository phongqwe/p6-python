from typing import Optional, Tuple

from com.emeraldblast.p6.document_structure.cell.Cell import Cell
from com.emeraldblast.p6.document_structure.cell.address.CellAddress import CellAddress
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

    @property
    def rootWorksheet(self) -> 'Worksheet':
        return self._innerSheet.rootWorksheet

    @property
    def workbook(self) -> Workbook | None:
        return self._innerSheet.workbook

    @workbook.setter
    def workbook(self, newWorkbook: Workbook | None):
        self._innerSheet.workbook = newWorkbook

    @property
    def translator(self) -> FormulaTranslator:
        return self._innerSheet.translator
    @property
    def name(self) -> str:
        return self._innerSheet.name

    @property
    def size(self) -> int:
        return self._innerSheet.size

    def toJson(self) -> WorksheetJson:
        return self._innerSheet.toJson()

    def cell(self, address: str | CellAddress | Tuple[int, int]) -> Cell:
        return self._innerSheet.cell(address)

    def range(self, rangeAddress: str | RangeAddress | Tuple[CellAddress, CellAddress]) -> Range:
        return self._innerSheet.range(rangeAddress)

    def addCell(self, cell: Cell):
        self._innerSheet.addCell(cell)

    def removeCell(self, address: CellAddress):
        self._innerSheet.removeCell(address)

    def getOrMakeCell(self, address: CellAddress) -> Cell:
        return self._innerSheet.getOrMakeCell(address)

    def hasCellAt(self, address: CellAddress) -> bool:
        return self._innerSheet.hasCellAt(address)

    def getCell(self, address: CellAddress) -> Optional[Cell]:
        return self._innerSheet.getCell(address)

    def isEmpty(self) -> bool:
        return self._innerSheet.isEmpty()

    def containsAddress(self, address: CellAddress) -> bool:
        return self._innerSheet.containsAddress(address)

    @property
    def cells(self) -> list[Cell]:
        return self._innerSheet.cells

    @property
    def rangeAddress(self) -> RangeAddress:
        return self._innerSheet.rangeAddress

    def toJsonDict(self) -> dict:
        return self._innerSheet.toJsonDict()

    def reportJsonStr(self) -> str:
        return self._innerSheet.reportJsonStr()

    def isSameRangeAddress(self, other):
        return self._innerSheet.isSameRangeAddress(other)

    def reRun(self):
        self._innerSheet.reRun()

    @property
    def innerSheet(self):
        return self._innerSheet

    def internalRename(self, newName: str):
        self._innerSheet.internalRename(newName)

    def renameRs(self, newName: str) -> Result[None, ErrorReport]:
        return self._innerSheet.renameRs(newName)
