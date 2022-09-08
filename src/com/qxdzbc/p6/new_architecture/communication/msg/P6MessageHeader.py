from com.qxdzbc.p6.document_structure.util.ToProto import ToProto
from com.qxdzbc.p6.new_architecture.communication.msg.P6Event import P6Event
from com.qxdzbc.p6.proto.P6MsgProtos_pb2 import P6MessageHeaderProto


class P6MessageHeader(ToProto[P6MessageHeaderProto]):

    def __init__(self, msgId: str, eventType: P6Event):
        self._msgId = msgId
        self._msgType:P6Event = eventType

    @staticmethod
    def fromProto(proto:P6MessageHeaderProto)->'P6MessageHeader':
        rt = P6MessageHeader(
            msgId = proto.msgId,
            eventType = P6Event(
                code = proto.eventType.code,
                name = proto.eventType.name
            )
        )
        return rt

    def toProtoObj(self) -> P6MessageHeaderProto:
        rt = P6MessageHeaderProto()
        rt.msgId = self._msgId
        rt.eventType.CopyFrom(self._msgType.toProtoObj())
        return rt

    @property
    def msgId(self):
        return self._msgId

    @property
    def eventType(self)->P6Event:
        return self._msgType

    def __eq__(self, other):
        if isinstance(other,P6MessageHeader):
            return self.msgId == other.msgId and self.eventType == other.eventType
        else:
            return False