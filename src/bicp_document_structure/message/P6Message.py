import json

from bicp_document_structure.message.P6MessageHeader import P6MessageHeader
from bicp_document_structure.message.proto.P6MsgPM_pb2 import P6MessageProto
from bicp_document_structure.util.ToJson import ToJson
from bicp_document_structure.util.ToProto import ToProto


class P6Message(ToProto[P6MessageProto]):

    def __init__(self, header: P6MessageHeader, content: ToProto | str | bytes):
        self._content: ToProto | str | bytes = content
        self._header: P6MessageHeader = header

    @property
    def content(self):
        return self._content

    @property
    def header(self):
        return self._header

    def toProtoObj(self):
        rt = P6MessageProto()
        rt.header.CopyFrom(self.header.toProtoObj())
        content = self.content
        if isinstance(self.content, ToProto):
            content = self.content.toProtoBytes()
        rt.data = content
        return rt
