from com.qxdzbc.p6.document_structure.formula_translator.FormulaTranslator import FormulaTranslator
from com.qxdzbc.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.qxdzbc.p6.document_structure.util.result.Ok import Ok
from com.qxdzbc.p6.document_structure.util.result.Result import Result


class MockTranslator( FormulaTranslator):
    """for testing only"""
    def translate(self, formula: str) -> Result[str, ErrorReport]:
        return Ok(formula)