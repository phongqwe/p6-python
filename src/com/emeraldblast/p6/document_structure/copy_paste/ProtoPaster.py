import ast
from abc import ABC

import pandas
import pyperclip

from com.emeraldblast.p6.document_structure.communication.event.data_structure.range_event.RangeCopy import RangeCopy

class ProtoPaster(ABC):
    def pasteRange(self)->RangeCopy:
        # df = pandas.read_clipboard()
        # protoBytesStr = df.iloc[0][0]
        protoBytesStr = pyperclip.paste()
        protoBytes=ast.literal_eval(protoBytesStr)
        return RangeCopy.fromProtoBytes(protoBytes)
