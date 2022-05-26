import zmq
from zmq import Socket

from com.emeraldblast.p6.document_structure.communication.SocketProvider import SocketProvider
from com.emeraldblast.p6.document_structure.communication.event_server.msg.P6Message import P6Message
from com.emeraldblast.p6.document_structure.communication.event_server.response.P6Response import P6Response
from com.emeraldblast.p6.document_structure.communication.sender.MessageSenderErrors import MessageSenderErrors
from com.emeraldblast.p6.document_structure.util.ToProto import ToProto
from com.emeraldblast.p6.document_structure.util.report.error.ErrorReport import ErrorReport
from com.emeraldblast.p6.document_structure.util.result.Err import Err
from com.emeraldblast.p6.document_structure.util.result.Ok import Ok
from com.emeraldblast.p6.document_structure.util.result.Result import Result


class MessageSender:
    @staticmethod
    def sendP6MsgRes(socketProvider: SocketProvider | None, p6Msg: P6Message | P6Response):
        """ send a p6msg/p6response """
        if socketProvider is not None:
            socket = socketProvider.notificationSocket()
            if socket is not None:
                replyRs = MessageSender.sendREQ_Proto(
                    socket = socket,
                    msg = p6Msg)
                if replyRs.isErr():
                    raise replyRs.err.toException()

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
                return Err(MessageSenderErrors.FailToSend("Fail to send: " + str(msg.toProtoObj())))
