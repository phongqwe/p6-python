
import pyperclip

from com.emeraldblast.p6.document_structure.copy_paste.copier.Copier import Copier
from com.emeraldblast.p6.document_structure.copy_paste.CopyPasteErrors import CopyPasteErrors
from com.emeraldblast.p6.document_structure.range.Range import Range
from com.emeraldblast.p6.document_structure.util.result.Err import Err
from com.emeraldblast.p6.document_structure.util.result.Ok import Ok


class ProtoCopier(Copier):
    def copyRangeToClipboard(self,rng:Range):
        try:
            protoBytes = rng.toRangeCopy().toProtoBytes()
            pyperclip.copy(str(protoBytes))
            return Ok(None)
        except Exception as e:
            return Err(CopyPasteErrors.UnableToCopyRange.report(rng.id))

