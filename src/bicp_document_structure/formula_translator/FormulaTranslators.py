from typing import Optional

from bicp_document_structure.formula_translator.FormulaTranslator import FormulaTranslator
from bicp_document_structure.formula_translator.MockTranslator import MockTranslator
from bicp_document_structure.formula_translator.StdFormulaTranslator import StdFormulaTranslator
from bicp_document_structure.formula_translator.WbWsFormulaTranslatorFinal import WbWsFormulaTranslator
from bicp_document_structure.workbook.WorkbookKey import WorkbookKey


class FormulaTranslators:
    __standard: Optional[FormulaTranslator] = None

    @staticmethod
    def standard() -> FormulaTranslator:
        if FormulaTranslators.__standard is None:
            FormulaTranslators.__standard = StdFormulaTranslator()
        return FormulaTranslators.__standard

    @staticmethod
    def standardWbWs(worksheetName: str | None, workbookKey: WorkbookKey | None) -> FormulaTranslator:
        return WbWsFormulaTranslator(worksheetName, workbookKey)

    @staticmethod
    def mock():
        """for testing only"""
        return MockTranslator()