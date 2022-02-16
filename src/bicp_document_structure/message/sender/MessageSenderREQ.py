from zmq import Socket

from bicp_document_structure.message.P6Message import P6Message
from bicp_document_structure.message.sender.MessageSender import MessageSender
from bicp_document_structure.message.sender.MessageSenderErrors import MessageSenderErrors
from bicp_document_structure.util.report.error.ErrorReport import ErrorReport
from bicp_document_structure.util.result.Err import Err
from bicp_document_structure.util.result.Ok import Ok
from bicp_document_structure.util.result.Result import Result


class MessageSenderREQ(MessageSender):
    def __init__(self, reqSocket: Socket):
        self.reqSocket = reqSocket

    def send(self, message: P6Message) -> Result[None, ErrorReport]:
        self.reqSocket.send(message.toBytes())
        reply = self.reqSocket.recv()
        replyStr = reply.decode()
        if replyStr.lower() == "ok":
            return Ok(None)
        else:
            return Err(ErrorReport(
                header = MessageSenderErrors.FailToSend.header,
                data = MessageSenderErrors.FailToSend.Data(message)
            ))
