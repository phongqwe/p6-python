from bicp_document_structure.common.ToJsonStr import ToJson
from bicp_document_structure.message.MsgType import MsgType


class P6MessageHeader(ToJson):

    def __init__(self, msgId:str, msgType:MsgType):
        self._msgId = msgId
        self._msgType = msgType

    @property
    def msgId(self):
        return self._msgId

    @property
    def msgType(self):
        return self._msgType

    def toJsonDict(self) -> dict:
        return {
            "msgId":self.msgId,
            "msgType":self.msgType.value
        }
