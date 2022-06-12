import ast

import pyperclip

from com.emeraldblast.p6.document_structure.communication.event.data_structure.range_event.RangeCopy import RangeCopy
from com.emeraldblast.p6.document_structure.copy_paste.BasePaster import BasePaster
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.emeraldblast.p6.document_structure.util.result.Ok import Ok
from com.emeraldblast.p6.document_structure.util.result.Result import Result


class ProtoPaster(BasePaster):
    def doPaste(self) -> Result[RangeCopy, ErrorReport]:
        protoBytesStr = pyperclip.paste()
        protoBytes = ast.literal_eval(protoBytesStr)
        o = RangeCopy.fromProtoBytes(protoBytes)
        return Ok(o)
