from abc import ABC

import pandas
import pyperclip

from com.emeraldblast.p6.document_structure.copy_paste.Copier import Copier
from com.emeraldblast.p6.document_structure.range.Range import Range


class PandasProtoCopier(Copier):
    def copyRangeToClipboard(self,rng:Range):
        protoBytes = rng.toRangeCopy().toProtoBytes()
        df=pandas.DataFrame([protoBytes],dtype = "bytes")
        df.to_clipboard()
