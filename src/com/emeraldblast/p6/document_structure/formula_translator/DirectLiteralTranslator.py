import re

from com.emeraldblast.p6.document_structure.formula_translator.FormulaTranslator import FormulaTranslator
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.emeraldblast.p6.document_structure.util.result.Ok import Ok
from com.emeraldblast.p6.document_structure.util.result.Result import Result


class DirectLiteralTranslator(FormulaTranslator):
    """
    This translator handles literal input such as number, string
    """

    stringPattern = re.compile("^\".*\"$",
                               re.IGNORECASE | re.DOTALL | re.MULTILINE | re.UNICODE)

    def translate(self, formula: str) -> Result[str,ErrorReport]:
        """
        :param formula:
        :return if the original formula is a number, return it. if it is a string, put it in a double quote and return the new string. Otherwise, return error obj
        """
        i = None

        try:
            i = float(formula)
        except ValueError:
            i = None

        if i is not None:
            return Ok(formula)
        else:
            isStringLiteral = DirectLiteralTranslator.stringPattern.fullmatch(formula) is not None
            if isStringLiteral:
                return Ok("\"\"{f}\"\"".format(f=formula))
            else:
                return Ok("\"\"\"{f}\"\"\"".format(f=formula))
