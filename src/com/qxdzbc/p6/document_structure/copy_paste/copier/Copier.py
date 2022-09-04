from abc import ABC
from typing import TYPE_CHECKING

from com.qxdzbc.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.qxdzbc.p6.document_structure.util.result.Result import Result

if TYPE_CHECKING:
    from com.qxdzbc.p6.document_structure.range.Range import Range

class Copier(ABC):
    def copyRangeToClipboard(self,rng:'Range')->Result[None,ErrorReport]:
        raise NotImplementedError()