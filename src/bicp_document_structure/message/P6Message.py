import json

from bicp_document_structure.message.P6MessageHeader import P6MessageHeader
from bicp_document_structure.util.ToJson import ToJson
from bicp_document_structure.util.ToProto import ToProto


class P6Message(ToJson):

    def __init__(self, header: P6MessageHeader, content: ToJson | ToProto):
        self._content: ToJson | ToProto = content
        self._header: P6MessageHeader = header

    @property
    def content(self):
        return self._content

    @property
    def header(self):
        return self._header

    def toJsonDict(self) -> dict:
        content = ""

        if isinstance(self.content, ToJson):
            content = self.content.toJsonStr()

        return {
            "header": self.header.toJsonDict(),
            "content": {
                "data": content
            }
        }

    def toProtoJsonDict(self) -> dict:
        content = ""
        if isinstance(self.content, ToProto):
            content = self.content.toProtoStr()
        return {
            "header": self.header.toJsonDict(),
            "content": {
                "data": content
            }
        }

    def toProtoJsonStr(self) -> str:
        return json.dumps(self.toProtoJsonDict())

    def toBytes(self):
        return bytes(self.toJsonStr().encode("UTF-8"))

    def toProtoBytes(self):
        return bytes(self.toProtoJsonStr().encode("UTF-8"))
