
import pyperclip

from com.emeraldblast.p6.document_structure.copy_paste.Copier import Copier
from com.emeraldblast.p6.document_structure.range.Range import Range


class ProtoCopier(Copier):
    def copyRangeToClipboard(self,rng:Range):
        protoBytes = rng.toRangeCopy().toProtoBytes()
        pyperclip.copy(str(protoBytes))
