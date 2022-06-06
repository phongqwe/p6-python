from abc import ABC

from com.emeraldblast.p6.document_structure.range.Range import Range
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.emeraldblast.p6.document_structure.util.result.Result import Result


class Copier(ABC):
    def copyRangeToClipboard(self,rng:Range)->Result[None,ErrorReport]:
        raise NotImplementedError()