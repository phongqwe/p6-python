from abc import ABC

from bicp_document_structure.common.ToJsonStr import ToJsonStr
from bicp_document_structure.message.P6Message import P6Message


class MessageConverter(ABC):
    def convert(self,jsonData:ToJsonStr)->P6Message:
        raise NotImplementedError()