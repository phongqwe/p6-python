from abc import ABC

from com.qxdzbc.p6.document_structure.copy_paste.CopyPasteErrors import CopyPasteErrors
from com.qxdzbc.p6.document_structure.copy_paste.copier.Copier import Copier
from com.qxdzbc.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.qxdzbc.p6.document_structure.util.result.Err import Err
from com.qxdzbc.p6.document_structure.util.result.Result import Result
from com.qxdzbc.p6.document_structure.range import Range

class BaseCopier(Copier,ABC):
    def copyRangeToClipboard(self, rng: Range.Range) -> Result[None, ErrorReport]:
        try:
            return self.doCopy(rng)
        except Exception as e:
            return Err(CopyPasteErrors.UnableToCopyRange.report(rng.id))

    def doCopy(self, rng: Range.Range) -> Result[None, ErrorReport]:
        raise NotImplementedError()