from bicp_document_structure.formula_translator.DirectLiteralTranslator import DirectLiteralTranslator
from bicp_document_structure.formula_translator.FormulaTranslator import FormulaTranslator
from bicp_document_structure.formula_translator.PythonFormulaTranslator import PythonFormulaTranslator
from bicp_document_structure.formula_translator.PythonFormulaVisitor import PythonFormulaVisitor
from bicp_document_structure.formula_translator.WithWbWsVisitor import WithWbWsVisitor
from bicp_document_structure.util.report.error.ErrorReport import ErrorReport
from bicp_document_structure.util.result.Result import Result
from bicp_document_structure.workbook.WorkbookKey import WorkbookKey


class WbWsFormulaTranslatorFinal(FormulaTranslator):

    def __init__(self, worksheetName: str | None = None, workbookKey: WorkbookKey | None = None):
        self.wsName: str | None = worksheetName
        self.wbKey: WorkbookKey | None = workbookKey
        self.pythonTranslator = PythonFormulaTranslator(
            visitor = WithWbWsVisitor(
                sheetName =self.wsName,
                workbookKey = self.wbKey,
                visitor = PythonFormulaVisitor()
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
