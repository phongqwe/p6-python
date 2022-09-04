from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING, Optional

from com.qxdzbc.p6.document_structure.cell.address.CellAddress import CellAddress
from com.qxdzbc.p6.document_structure.cell_container.MutableCellContainer import MutableCellContainer
from com.qxdzbc.p6.document_structure.cell_container.UserFriendlyCellContainer import UserFriendlyCellContainer

from com.qxdzbc.p6.document_structure.formula_translator.FormulaTranslator import FormulaTranslator
from com.qxdzbc.p6.document_structure.range.address.RangeAddress import RangeAddress
from com.qxdzbc.p6.document_structure.util.ToJson import ToJson
from com.qxdzbc.p6.document_structure.util.ToProto import ToProto
from com.qxdzbc.p6.document_structure.util.report.ReportJsonStrMaker import ReportJsonStrMaker
from com.qxdzbc.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.qxdzbc.p6.document_structure.util.result.Result import Result
from com.qxdzbc.p6.document_structure.worksheet.UserFriendlyWorksheet import UserFriendlyWorksheet
from com.qxdzbc.p6.document_structure.worksheet.WorksheetJson import WorksheetJson
from com.qxdzbc.p6.proto.DocProtos_pb2 import WorksheetProto

if TYPE_CHECKING:
    from com.qxdzbc.p6.document_structure.workbook.WorkBook import Workbook
    from com.qxdzbc.p6.document_structure.range.Range import Range
    from com.qxdzbc.p6.document_structure.cell.Cell import Cell
    from com.qxdzbc.p6.document_structure.copy_paste.paster.Paster import Paster


class Worksheet(UserFriendlyCellContainer,
                UserFriendlyWorksheet,
                MutableCellContainer,
                ReportJsonStrMaker,
                ToJson,
                ToProto[WorksheetProto],
                ABC):

    @property
    def colDict(self) -> dict[int, list[Cell]]:
        raise NotImplementedError()

    @property
    def rowDict(self) -> dict[int, list[Cell]]:
        raise NotImplementedError()

    @property
    def maxUsedCol(self) -> int | None:
        raise NotImplementedError()

    @property
    def minUsedCol(self) -> int | None:
        raise NotImplementedError()

    @property
    def maxUsedRow(self) -> int | None:
        raise NotImplementedError()

    @property
    def minUsedRow(self) -> int | None:
        raise NotImplementedError()

    @property
    def usedRangeAddress(self) -> RangeAddress | None:
        raise NotImplementedError()

    @property
    def usedRange(self) -> Range | None:
        raise NotImplementedError()

    def pasteDataFrame(self, anchorCell: CellAddress, paster: Paster | None=None):
        raise NotImplementedError()

    def pasteDataFrameRs(self, anchorCell: CellAddress, paster: Paster | None=None) -> Result[None, ErrorReport]:
        raise NotImplementedError()

    def pasteProto(self, cell: CellAddress, paster: Paster | None = None):
        raise NotImplementedError()

    def pasteProtoRs(
            self,
            cell: CellAddress,
            paster: Paster | None = None) -> Result[None, ErrorReport]:
        raise NotImplementedError()

    def pasteRs(self,
                cell: CellAddress,
                paster: Paster | None = None) -> Result[None, ErrorReport]:
        """paste what inside the system clipboard into the sheet, starting at a cell"""
        raise NotImplementedError()

    def paste(self,
              cell: CellAddress,
              paster: Paster | None = None):
        raise NotImplementedError()

    def compareContent(self, ws2: Worksheet) -> bool:
        """Compare equality by comparing name and comparing all cell of this sheet with another. Very inefficient, use with care"""
        raise NotImplementedError()

    @property
    def cellCount(self):
        raise NotImplementedError()

    @property
    def rootWorksheet(self) -> 'Worksheet':
        """the root worksheet is the lowest layer (data layer) worksheet, not hooked to any event callbacks, not wrapped in any wrapper. For data-layer worksheet, this is itself. For wrapper worksheet, this is their inner worksheet"""
        raise NotImplementedError()

    def toProtoObj(self) -> WorksheetProto:
        raise NotImplementedError()

    @property
    def workbook(self) -> Optional[Workbook]:
        raise NotImplementedError()

    @workbook.setter
    def workbook(self, newWorkbook: Optional[Workbook]):
        raise NotImplementedError()

    def removeFromWorkbook(self):
        raise NotImplementedError()

    @property
    def name(self) -> str:
        raise NotImplementedError()

    @property
    def translator(self) -> FormulaTranslator:
        raise NotImplementedError()

    def toJson(self) -> WorksheetJson:
        raise NotImplementedError()

    def reportJsonStr(self) -> str:
        raise NotImplementedError()

    def rename(self, newName: str):
        raise NotImplementedError()

    def internalRename(self, newName: str):
        # todo delete this
        raise NotImplementedError()

    def renameRs(self, newName: str) -> Result[None, ErrorReport]:
        raise NotImplementedError()
