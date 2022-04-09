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
