import re

from bicp_document_structure.formula_translator.FormulaTranslator import FormulaTranslator
from bicp_document_structure.util.result.Ok import Ok
from bicp_document_structure.util.result.Result import Result


class DirectLiteralTranslator(FormulaTranslator):
    strPattern = re.compile("^\".*\"$",
                            re.IGNORECASE | re.DOTALL | re.MULTILINE | re.UNICODE)

    def translate(self, formula: str) -> Result:
        i = None

        try:
            i = float(formula)
        except ValueError:
            i = None

        if i is not None:
            return Ok(formula)
        else:
            isStringLiteral = DirectLiteralTranslator.strPattern.fullmatch(formula) is not None
            if isStringLiteral:
                return Ok("\"\"{f}\"\"".format(f=formula))
            else:
                return Ok("\"\"\"{f}\"\"\"".format(f=formula))