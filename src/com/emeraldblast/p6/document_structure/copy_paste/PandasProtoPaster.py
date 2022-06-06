from abc import ABC

import pandas

from com.emeraldblast.p6.document_structure.code_executor.CodeExecutor import CodeExecutor
from com.emeraldblast.p6.document_structure.communication.event.data_structure.range_event.RangeCopy import RangeCopy

from com.emeraldblast.p6.document_structure.range.Range import Range


class PandasProtoPaster(ABC):
    def pasteRange(self)->RangeCopy:
        df = pandas.read_clipboard()
        protoBytesStr = df.iloc[0][0]
        protoBytes = CodeExecutor.evalCode(protoBytesStr, {}, {})
        return RangeCopy.fromProtoBytes(protoBytes)
