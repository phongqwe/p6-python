from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING

from com.emeraldblast.p6.document_structure.cell.address.CellAddress import CellAddress
from com.emeraldblast.p6.document_structure.cell_container.MutableCellContainer import MutableCellContainer
from com.emeraldblast.p6.document_structure.cell_container.UserFriendlyCellContainer import UserFriendlyCellContainer

from com.emeraldblast.p6.document_structure.formula_translator.FormulaTranslator import FormulaTranslator
from com.emeraldblast.p6.document_structure.range.address.RangeAddress import RangeAddress
from com.emeraldblast.p6.document_structure.util.ToJson import ToJson
from com.emeraldblast.p6.document_structure.util.ToProto import ToProto
from com.emeraldblast.p6.document_structure.util.report.ReportJsonStrMaker import ReportJsonStrMaker
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.emeraldblast.p6.document_structure.util.result.Result import Result
from com.emeraldblast.p6.document_structure.worksheet.UserFriendlyWorksheet import UserFriendlyWorksheet
from com.emeraldblast.p6.document_structure.worksheet.WorksheetJson import WorksheetJson
from com.emeraldblast.p6.proto.DocProtos_pb2 import WorksheetProto

if TYPE_CHECKING:
    from com.emeraldblast.p6.document_structure.workbook.WorkBook import Workbook
    from com.emeraldblast.p6.document_structure.range.Range import Range
    from com.emeraldblast.p6.document_structure.cell.Cell import Cell
    from com.emeraldblast.p6.document_structure.copy_paste.Paster import Paster


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

    def pasteTextRs(self, targetCell: CellAddress, paster: Paster | None) -> Result[None, ErrorReport]:
        raise NotImplementedError()

    def pasteText(self, targetCell: CellAddress, paster: Paster | None):
        raise NotImplementedError()

    def pasteDataFrame(self, anchorCell: CellAddress, paster: Paster | None=None):
        raise NotImplementedError()

    def pasteDataFrameRs(self, anchorCell: CellAddress, paster: Paster | None=None) -> Result[None, ErrorReport]:
        raise NotImplementedError()

    def pasteProto(self, anchorCell: CellAddress, paster: Paster | None = None):
        raise NotImplementedError()

    def pasteProtoRs(
            self,
            anchorCell: CellAddress,
            paster: Paster | None = None) -> Result[None, ErrorReport]:
        raise NotImplementedError()

    def compareWith(self, ws2: Worksheet) -> bool:
        """compare all cell of this sheet with another. Very inefficient, use with care"""
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
    def workbook(self) -> Workbook | None:
        raise NotImplementedError()

    @workbook.setter
    def workbook(self, newWorkbook: Workbook | None):
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
        raise NotImplementedError()

    def renameRs(self, newName: str) -> Result[None, ErrorReport]:
        raise NotImplementedError()
