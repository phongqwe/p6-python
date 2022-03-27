import json
from abc import ABC

from bicp_document_structure.cell_container.MutableCellContainer import MutableCellContainer
from bicp_document_structure.cell_container.UserFriendlyCellContainer import UserFriendlyCellContainer
from bicp_document_structure.formula_translator.FormulaTranslator import FormulaTranslator
from bicp_document_structure.message.proto.DocProto_pb2 import WorksheetProto
from bicp_document_structure.util.ToJson import ToJson
from bicp_document_structure.util.ToProto import ToProto
from bicp_document_structure.util.report.ReportJsonStrMaker import ReportJsonStrMaker
from bicp_document_structure.worksheet.UserFriendlyWorksheet import UserFriendlyWorksheet
from bicp_document_structure.worksheet.WorksheetJson import WorksheetJson


class Worksheet(UserFriendlyCellContainer,
                UserFriendlyWorksheet,
                MutableCellContainer,
                ReportJsonStrMaker,
                ToJson,
                ToProto[WorksheetProto],
                ABC):

    def toProtoObj(self) -> WorksheetProto:
        rt = WorksheetProto()
        rt.name = self.name
        cells = []
        for cell in self.cells:
            cells.append(cell.toProtoObj())
        rt.cell.extend(cells)
        return rt

    @property
    def name(self) -> str:
        raise NotImplementedError()

    @property
    def translator(self) -> FormulaTranslator:
        raise NotImplementedError()

    def toJson(self)->WorksheetJson:
        raise NotImplementedError()

    def reportJsonStr(self) -> str:
        return json.dumps({
            "name":self.name
        })
    def rename(self,newName:str):
        raise NotImplementedError()