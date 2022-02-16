from abc import ABC

from bicp_document_structure.common.ToJsonStr import ToJson
from bicp_document_structure.message.MsgType import MsgType
from bicp_document_structure.message.P6Message import P6Message


class MessageConverter(ABC):
    def convert(self, msgType: MsgType, jsonData: ToJson) -> P6Message:
        raise NotImplementedError()
