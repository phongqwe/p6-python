import ast

import pyperclip

from com.emeraldblast.p6.document_structure.communication.event.data_structure.range_event.RangeCopy import RangeCopy
from com.emeraldblast.p6.document_structure.copy_paste.CopyErrors import CopyErrors
from com.emeraldblast.p6.document_structure.copy_paste.Paster import Paster
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.emeraldblast.p6.document_structure.util.result.Err import Err
from com.emeraldblast.p6.document_structure.util.result.Ok import Ok
from com.emeraldblast.p6.document_structure.util.result.Result import Result


class ProtoPaster(Paster):

    def pasteRange(self)->Result[RangeCopy,ErrorReport]:
        try:
            protoBytesStr = pyperclip.paste()
            protoBytes=ast.literal_eval(protoBytesStr)
            return Ok(RangeCopy.fromProtoBytes(protoBytes))
        except Exception as e:
            return Err(CopyErrors.UnableToPasteRange.report())

    def pasteText(self) -> Result[None, ErrorReport]:
        # todo implement this
        raise NotImplementedError()