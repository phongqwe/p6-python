from bicp_document_structure.message.P6MessageHeader import P6MessageHeader
from bicp_document_structure.util.ToJson import ToJson


class P6Message(ToJson):

    def __init__(self, header: P6MessageHeader, content: ToJson):
        self._content: ToJson = content
        self._header: P6MessageHeader = header

    @property
    def content(self):
        return self._content

    @property
    def header(self):
        return self._header

    def toJsonDict(self) -> dict:
        return {
            "header": self.header.toJsonDict(),
            "content": {
                "data":self.content.toJsonStr()
            }
        }
    def toBytes(self):
        return bytes(self.toJsonStr().encode("UTF-8"))