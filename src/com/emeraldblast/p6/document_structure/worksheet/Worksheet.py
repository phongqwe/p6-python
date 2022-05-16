from __future__ import annotations

import json
from abc import ABC
from typing import TYPE_CHECKING

from com.emeraldblast.p6.document_structure.cell_container.MutableCellContainer import MutableCellContainer
from com.emeraldblast.p6.document_structure.cell_container.UserFriendlyCellContainer import UserFriendlyCellContainer
from com.emeraldblast.p6.document_structure.formula_translator.FormulaTranslator import FormulaTranslator
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

class Worksheet(UserFriendlyCellContainer,
                UserFriendlyWorksheet,
                MutableCellContainer,
                ReportJsonStrMaker,
                ToJson,
                ToProto[WorksheetProto],
                ABC):

    def compareWith(self, ws2: Worksheet) -> bool:
        """compare all cell of this sheet with another. Very inefficient, use with care"""
        ws1 = self.rootWorksheet
        ws2 = ws2.rootWorksheet
        sameName = ws1.name == ws2.name
        if sameName:
            sameCellCount = ws1.cellCount == ws1.cellCount
            if sameCellCount:
                z = True
                for c1 in ws1.cells:
                    c2 = ws2.cell(c1.address)
                    if c1 != c2:
                        return False

                for c2 in ws2.cells:
                    c1 = ws1.cell(c2.address)
                    if c2 != c1:
                        return False
                return z
            else:
                return False
        else:
            return False

    @property
    def cellCount(self):
        return self.size

    @property
    def rootWorksheet(self)->'Worksheet':
        """the root worksheet is the lowest layer (data layer) worksheet, not hooked to any event callbacks, not wrapped in any wrapper. For data-layer worksheet, this is itself. For wrapper worksheet, this is their inner worksheet"""
        raise NotImplementedError()

    def toProtoObj(self) -> WorksheetProto:
        rt = WorksheetProto()
        rt.name = self.name
        cells = []
        for cell in self.cells:
            cells.append(cell.toProtoObj())
        rt.cell.extend(cells)
        return rt

    @property
    def workbook(self) -> Workbook | None:
        raise NotImplementedError()

    @workbook.setter
    def workbook(self, newWorkbook:Workbook | None):
        raise NotImplementedError()

    def removeFromWorkbook(self):
        self.workbook = None

    @property
    def name(self) -> str:
        raise NotImplementedError()

    @property
    def translator(self) -> FormulaTranslator:
        raise NotImplementedError()

    def toJson(self) -> WorksheetJson:
        raise NotImplementedError()

    def reportJsonStr(self) -> str:
        return json.dumps({
            "name": self.name
        })

    def rename(self, newName: str):
        rs = self.renameRs(newName)
        if rs.isErr():
            raise rs.err.toException()

    def internalRename(self, newName: str):
        raise NotImplementedError

    def renameRs(self, newName: str) -> Result[None, ErrorReport]:
        raise NotImplementedError()
