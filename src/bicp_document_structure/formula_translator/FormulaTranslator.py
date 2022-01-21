from abc import ABC

from bicp_document_structure.util.result.Result import Result


class FormulaTranslator(ABC):
    def translate(self, formula:str)->Result:
        raise NotImplementedError