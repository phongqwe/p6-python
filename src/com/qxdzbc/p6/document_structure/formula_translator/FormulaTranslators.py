from typing import Optional

from com.qxdzbc.p6.document_structure.formula_translator.FormulaTranslator import FormulaTranslator
from com.qxdzbc.p6.document_structure.formula_translator.MockTranslator import MockTranslator
from com.qxdzbc.p6.document_structure.formula_translator.StdFormulaTranslator import StdFormulaTranslator
from com.qxdzbc.p6.document_structure.formula_translator.WbWsFormulaTranslator import WbWsFormulaTranslator
from com.qxdzbc.p6.document_structure.workbook.key.WorkbookKey import WorkbookKey


class FormulaTranslators:
    __standard: Optional[FormulaTranslator] = None

    @staticmethod
    def standard() -> FormulaTranslator:
        if FormulaTranslators.__standard is None:
            FormulaTranslators.__standard = StdFormulaTranslator()
        return FormulaTranslators.__standard

    @staticmethod
    def standardWbWs(worksheetName: Optional[str], workbookKey: WorkbookKey) -> FormulaTranslator:
        return WbWsFormulaTranslator(worksheetName, workbookKey)

    @staticmethod
    def mock():
        """for testing only"""
        return MockTranslator()