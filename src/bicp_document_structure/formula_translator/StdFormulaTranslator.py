from bicp_document_structure.formula_translator.DirectLiteralTranslator import DirectLiteralTranslator
from bicp_document_structure.formula_translator.FormulaTranslator import FormulaTranslator
from bicp_document_structure.formula_translator.PythonFormulaTranslator import PythonFormulaTranslator
from bicp_document_structure.formula_translator.PythonFormulaVisitor import PythonFormulaVisitor
from bicp_document_structure.util.report.error.ErrorReport import ErrorReport
from bicp_document_structure.util.result.Result import Result


class StdFormulaTranslator(FormulaTranslator):

    def __init__(self):
        self.pythonTranslator = PythonFormulaTranslator(visitor = PythonFormulaVisitor())
        self.directLiteralTranslator = DirectLiteralTranslator()

    def translate(self, formula: str) -> Result[str,ErrorReport]:
        trimmed = formula.strip()
        isFormula = trimmed.startswith("=")
        if isFormula:
            return self.pythonTranslator.translate(formula)
        else:
            return self.directLiteralTranslator.translate(formula)
