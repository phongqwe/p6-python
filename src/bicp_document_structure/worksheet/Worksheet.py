import json
from abc import ABC

from bicp_document_structure.cell_container.MutableCellContainer import MutableCellContainer
from bicp_document_structure.cell_container.UserFriendlyCellContainer import UserFriendlyCellContainer
from bicp_document_structure.column.MutableColumnContainer import MutableColumnContainer
from bicp_document_structure.common.ToJsonStr import ToJson
from bicp_document_structure.formula_translator.FormulaTranslator import FormulaTranslator
from bicp_document_structure.util.report.ReportJsonStrMaker import ReportJsonStrMaker
from bicp_document_structure.worksheet.UserFriendlyWorksheet import UserFriendlyWorksheet
from bicp_document_structure.worksheet.WorksheetJson import WorksheetJson


class Worksheet(UserFriendlyCellContainer,
                UserFriendlyWorksheet,
                MutableCellContainer,
                MutableColumnContainer,
                ReportJsonStrMaker,ToJson,
                ABC):
    @property
    def name(self) -> str:
        raise NotImplementedError()

    @property
    def translator(self) -> FormulaTranslator | None:
        raise NotImplementedError()

    def toJson(self)->WorksheetJson:
        raise NotImplementedError()

    def reportJsonStr(self) -> str:
        return json.dumps({
            "name":self.name
        })