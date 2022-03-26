import json

from bicp_document_structure.message.P6MessageHeader import P6MessageHeader
from bicp_document_structure.message.proto.P6MsgPM_pb2 import P6MessageProto
from bicp_document_structure.util.ToJson import ToJson
from bicp_document_structure.util.ToProto import ToProto


class P6Message(ToJson,ToProto[P6MessageProto]):

    def __init__(self, header: P6MessageHeader, content: ToJson | ToProto| str):
        self._content: ToJson | ToProto |str= content
        self._header: P6MessageHeader = header

    @property
    def isError(self):
        return self._header.isError

    @property
    def content(self):
        return self._content

    @property
    def header(self):
        return self._header

    def toJsonDict(self) -> dict:
        content =self.content

        if isinstance(self.content, ToJson):
            content = self.content.toJsonStr()

        return {
            "header": self.header.toJsonDict(),
            "content": {
                "data": content
            }
        }

    def toProtoJsonDict(self) -> dict:
        content =self.content
        if isinstance(self.content, ToProto):
            content = self.content.toProtoStr()
        return {
            "header": self.header.toJsonDict(),
            "content": {
                "data": content
            }
        }

    def toProtoJsonStr(self) -> str:
        """ only convert the inner data structure into proto, p6msg structure is still in json"""
        return json.dumps(self.toProtoJsonDict())

    def toBytes(self):
        return bytes(self.toJsonStr().encode("UTF-8"))

    def toProtoJsonBytes(self):
        return bytes(self.toProtoJsonStr().encode("UTF-8"))

    def toProtoObj(self):
        rt = P6MessageProto()
        rt.header.CopyFrom(self.header.toProtoObj())
        content = self.content
        if isinstance(self.content, ToProto):
            content = self.content.toProtoStr()
        rt.data = content
        return rt
