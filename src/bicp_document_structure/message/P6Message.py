from bicp_document_structure.common.ToJsonStr import ToJsonStr
from bicp_document_structure.message.P6MessageHeader import P6MessageHeader
from bicp_document_structure.message.P6RawMessage import RawMessage


class P6Message:
    def __init__(self, header: P6MessageHeader, content: ToJsonStr):
        self.content: ToJsonStr = content
        self.header: P6MessageHeader = header

    def toRawMsg(self) -> RawMessage:
        rt = RawMessage(
            self.header.toJsonStr(),
            self.content.toJsonStr(),
        )
        return rt
