from abc import ABC
from typing import Generic, TypeVar

from bicp_document_structure.message.P6Message import P6Message
from bicp_document_structure.util.report.error.ErrorReport import ErrorReport
from bicp_document_structure.util.result.Result import Result

R = TypeVar("R")

class MessageSender(ABC,Generic[R]):
    def send(self,message:P6Message)->Result[R,ErrorReport]:
        raise NotImplementedError()