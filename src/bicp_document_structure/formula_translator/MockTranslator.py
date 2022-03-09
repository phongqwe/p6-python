from bicp_document_structure.formula_translator.FormulaTranslator import FormulaTranslator
from bicp_document_structure.util.report.error.ErrorReport import ErrorReport
from bicp_document_structure.util.result.Ok import Ok
from bicp_document_structure.util.result.Result import Result


class MockTranslator( FormulaTranslator):
    def translate(self, formula: str) -> Result[str, ErrorReport]:
        return Ok(formula)