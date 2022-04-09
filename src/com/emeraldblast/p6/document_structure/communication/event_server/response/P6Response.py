import uuid
from enum import Enum
from typing import Any

from com.emeraldblast.p6.document_structure.communication.event_server.msg.P6MessageHeader import P6MessageHeader
from com.emeraldblast.p6.document_structure.util.ToProto import ToProto
from com.emeraldblast.p6.proto.P6MsgProtos_pb2 import P6ResponseProto


class P6Response(ToProto[P6ResponseProto]):
    class Status(Enum):
        INVALID = 0
        OK = 2
        ERROR = 3

        @staticmethod
        def fromProto(protoStatus:P6ResponseProto.Status)->'P6Response.Status':
            s = P6Response.Status
            o = P6ResponseProto.Status
            if protoStatus == o.OK:
                return s.OK
            elif protoStatus == o.ERROR:
                return s.ERROR
            else:
                return s.INVALID
        def toProto(self)->P6ResponseProto.Status:
            s = P6Response.Status
            o = P6ResponseProto.Status
            if self == s.OK:
                return o.OK
            elif self == s.ERROR:
                return o.ERROR
            else:
                return o.INVALID

    def __init__(self, header: P6MessageHeader, data: ToProto | str | bytes, status: 'P6Response.Status'):
        self._content: ToProto | str | bytes = data
        self._header: P6MessageHeader = header
        self._status = status

    @staticmethod
    def create(event, data: Any, status: 'P6Response.Status')->'P6Response':
        msg = P6Response(
            header = P6MessageHeader(
                msgId = str(uuid.uuid4()),
                eventType = event,
            ),
            data = data,
            status = status)
        return msg

    @staticmethod
    def fromProto(proto: P6ResponseProto) -> 'P6Response':
        rt = P6Response(
            header = P6MessageHeader.fromProto(proto.header),
            data = proto.data,
            status = P6Response.Status.fromProto(proto.status)
        )
        return rt

    @property
    def data(self):
        return self._content

    @property
    def header(self):
        return self._header
    @property
    def status(self)->'P6Response.Status':
        return self._status


    def toProtoObj(self):
        rt = P6ResponseProto()
        rt.header.CopyFrom(self.header.toProtoObj())
        content = self.data
        if isinstance(self.data, ToProto):
            content = self.data.toProtoBytes()
        rt.data = content
        rt.status = (self._status.toProto())
        return rt