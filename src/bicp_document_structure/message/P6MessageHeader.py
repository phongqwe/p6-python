from bicp_document_structure.message.event.P6Event import P6Event
from bicp_document_structure.message.proto.P6MsgPM_pb2 import P6MessageHeaderProto
from bicp_document_structure.util.ToJson import ToJson
from bicp_document_structure.util.ToProto import ToProto


class P6MessageHeader(ToProto[P6MessageHeaderProto]):

    def __init__(self, msgId: str, eventType: P6Event):
        self._msgId = msgId
        self._msgType = eventType

    def toProtoObj(self) -> P6MessageHeaderProto:
        rt = P6MessageHeaderProto()
        rt.msgId = self._msgId
        rt.eventType.CopyFrom(self._msgType.toProtoObj())
        return rt

    @property
    def msgId(self):
        return self._msgId

    @property
    def eventType(self):
        return self._msgType