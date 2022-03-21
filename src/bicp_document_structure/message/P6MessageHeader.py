from bicp_document_structure.event.P6Event import P6Event
from bicp_document_structure.util.ToJson import ToJson


class P6MessageHeader(ToJson):

    def __init__(self, msgId:str, eventType:P6Event):
        self._msgId = msgId
        self._msgType = eventType

    @property
    def msgId(self):
        return self._msgId

    @property
    def eventType(self):
        return self._msgType

    def toJsonDict(self) -> dict:
        return {
            "msgId":self.msgId,
            "msgType":self.eventType.msgRepresentation
        }
