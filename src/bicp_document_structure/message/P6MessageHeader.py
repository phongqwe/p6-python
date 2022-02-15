from bicp_document_structure.common.ToJsonStr import ToJsonStr
from bicp_document_structure.message.MsgType import MsgType


class P6MessageHeader(ToJsonStr):
    def toJsonStr(self) -> str:
        pass

    def __init__(self, msgId:str, msgType:MsgType):
        self.msgId = msgId
        self.msgType = msgType



