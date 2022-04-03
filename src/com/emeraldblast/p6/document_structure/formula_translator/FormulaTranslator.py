from abc import ABC

from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.emeraldblast.p6.document_structure.util.result.Result import Result


class FormulaTranslator(ABC):
    def translate(self, formula:str)->Result[str,ErrorReport]:
        raise NotImplementedError