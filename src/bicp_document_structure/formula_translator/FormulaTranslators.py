from typing import Optional

from bicp_document_structure.formula_translator.FormulaTranslator import FormulaTranslator
from bicp_document_structure.formula_translator.FormulaTranslatorFinal import FormulaTranslatorFinal


class FormulaTranslators:
    __standard:Optional[FormulaTranslator] = None
    @staticmethod
    def standard()->FormulaTranslator:
        if FormulaTranslators.__standard is None:
            FormulaTranslators.__standard = FormulaTranslatorFinal()
        return FormulaTranslators.__standard