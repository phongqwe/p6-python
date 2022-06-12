from abc import ABC

from com.emeraldblast.p6.document_structure.copy_paste.CopyErrors import CopyErrors

from com.emeraldblast.p6.document_structure.copy_paste.Copier import Copier
from com.emeraldblast.p6.document_structure.range.Range import Range
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.emeraldblast.p6.document_structure.util.result.Err import Err
from com.emeraldblast.p6.document_structure.util.result.Result import Result


class BaseCopier(Copier,ABC):
    def copyRangeToClipboard(self, rng: Range) -> Result[None, ErrorReport]:
        try:
            return self.doCopy(rng)
        except Exception as e:
            return Err(CopyErrors.UnableToCopyRange.report(rng.id))

    def doCopy(self, rng: Range) -> Result[None, ErrorReport]:
        raise NotImplementedError()