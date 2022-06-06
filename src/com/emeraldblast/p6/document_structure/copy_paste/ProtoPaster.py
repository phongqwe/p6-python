import ast

import pyperclip

from com.emeraldblast.p6.document_structure.communication.event.data_structure.range_event.RangeCopy import RangeCopy
from com.emeraldblast.p6.document_structure.copy_paste.Paster import Paster


class ProtoPaster(Paster):
    def pasteRange(self)->RangeCopy:
        protoBytesStr = pyperclip.paste()
        protoBytes=ast.literal_eval(protoBytesStr)
        return RangeCopy.fromProtoBytes(protoBytes)
