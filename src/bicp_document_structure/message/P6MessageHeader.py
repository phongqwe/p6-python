from bicp_document_structure.message.event.P6Event import P6Event
from bicp_document_structure.message.proto.P6MsgPM_pb2 import P6MessageHeaderProto
from bicp_document_structure.util.ToJson import ToJson
from bicp_document_structure.util.ToProto import ToProto


class P6MessageHeader(ToJson, ToProto[P6MessageHeaderProto]):

    def __init__(self, msgId: str, eventType: P6Event, isError: bool):
        self._msgId = msgId
        self._msgType = eventType
        self._isError = isError

    def toProtoObj(self) -> P6MessageHeaderProto:
        rt = P6MessageHeaderProto()
        rt.msgId = self._msgId
        rt.eventType.CopyFrom(self._msgType.toProtoObj())
        rt.isError = self.isError
        return rt

    @property
    def isError(self) -> bool:
        return self._isError

    @property
    def msgId(self):
        return self._msgId

    @property
    def eventType(self):
        return self._msgType

    def toJsonDict(self) -> dict:
        return {
            "msgId": self.msgId,
            "eventType": self.eventType.name
        }
