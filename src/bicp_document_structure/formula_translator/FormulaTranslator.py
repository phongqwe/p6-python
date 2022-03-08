from abc import ABC

from bicp_document_structure.util.report.error.ErrorReport import ErrorReport
from bicp_document_structure.util.result.Result import Result


class FormulaTranslator(ABC):
    def translate(self, formula:str)->Result[str,ErrorReport]:
        raise NotImplementedError