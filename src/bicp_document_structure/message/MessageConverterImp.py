import uuid
from abc import ABC

from bicp_document_structure.common.ToJsonStr import ToJson
from bicp_document_structure.message.MessageConverter import MessageConverter
from bicp_document_structure.message.MsgType import MsgType
from bicp_document_structure.message.P6Message import P6Message
from bicp_document_structure.message.P6MessageHeader import P6MessageHeader


class MessageConverterImp(MessageConverter, ABC):

    def convert(self, msgType: MsgType, jsonData: ToJson) -> P6Message:
        return P6Message(
            header=P6MessageHeader(str(uuid.uuid4()), msgType),
            content=jsonData
        )
