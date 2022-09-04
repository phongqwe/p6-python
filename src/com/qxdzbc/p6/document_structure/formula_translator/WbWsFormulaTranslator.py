from typing import Optional

from com.qxdzbc.p6.document_structure.formula_translator.DirectLiteralTranslator import DirectLiteralTranslator
from com.qxdzbc.p6.document_structure.formula_translator.FormulaTranslator import FormulaTranslator
from com.qxdzbc.p6.document_structure.formula_translator.PythonFormulaTranslator import PythonFormulaTranslator
from com.qxdzbc.p6.document_structure.formula_translator.WbWsVisitor import WbWsVisitor
from com.qxdzbc.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.qxdzbc.p6.document_structure.util.result.Result import Result
from com.qxdzbc.p6.document_structure.workbook.key.WorkbookKey import WorkbookKey


class WbWsFormulaTranslator(FormulaTranslator):
    """
    A translator with a workbook key. The output script of this translator always explicitly specify the workbook, worksheet it depends/runs on.
    """
    def __init__(self, worksheetName: Optional[str] = None, workbookKey: WorkbookKey | None = None):
        self.wsName: Optional[str] = worksheetName
        self.wbKey: WorkbookKey | None = workbookKey
        self.pythonTranslator = PythonFormulaTranslator(
            visitor = WbWsVisitor(
                sheetName =self.wsName,
                workbookKey = self.wbKey,
            )
        )
        self.directLiteralTranslator = DirectLiteralTranslator()

    def translate(self, formula: str) -> Result[str, ErrorReport]:
        trimmed = formula.strip()
        isFormula = trimmed.startswith("=")
        if isFormula:
            return self.pythonTranslator.translate(formula)
        else:
            return self.directLiteralTranslator.translate(formula)
