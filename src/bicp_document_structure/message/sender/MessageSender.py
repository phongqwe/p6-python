import zmq
from bicp_document_structure.util.ToProto import ToProto
from zmq import Socket

from bicp_document_structure.message.P6Message import P6Message
from bicp_document_structure.message.sender.MessageSenderErrors import MessageSenderErrors
from bicp_document_structure.util.report.error.ErrorReport import ErrorReport
from bicp_document_structure.util.result.Err import Err
from bicp_document_structure.util.result.Ok import Ok
from bicp_document_structure.util.result.Result import Result


class MessageSender:

    @staticmethod
    def sendREQ_Proto(socket: Socket, msg: ToProto) -> Result[None, ErrorReport]:
        """
        send a P6Message on a REQ socket and check for a boolean reply
        if reply is "ok", then the request is considered success, return err otherwise
        """
        if socket.type != zmq.REQ:
            return Err(
                ErrorReport(
                    header = MessageSenderErrors.WrongSocketType.header,
                    data = MessageSenderErrors.WrongSocketType.Data(socket.type, zmq.REQ)
                )
            )
        if socket is not None:
            socket.send(msg.toProtoBytes())
            reply = socket.recv()
            replyStr = reply.decode()
            if replyStr.lower() == "ok":
                return Ok(None)
            else:
                return Err(ErrorReport(
                    header = MessageSenderErrors.FailToSend.header,
                    data = MessageSenderErrors.FailToSend.Data(msg)
                ))
