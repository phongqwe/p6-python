from typing import Optional, Union

import zmq
from zmq import Socket

from com.qxdzbc.p6.util import ToProto
from com.qxdzbc.p6.util.report.error.ErrorReport import ErrorReport
from com.qxdzbc.p6.util.result.Err import Err
from com.qxdzbc.p6.util.result.Ok import Ok
from com.qxdzbc.p6.util.result.Result import Result
from com.qxdzbc.p6.communication.SocketProvider import SocketProvider
from com.qxdzbc.p6.communication.msg.P6Message import P6Message
from com.qxdzbc.p6.communication.response.P6Response import P6Response
from com.qxdzbc.p6.communication.sender.MessageSenderErrors import MessageSenderErrors


class MessageSender:
    @staticmethod
    def sendP6MsgRes(
            socketProvider: Optional[SocketProvider],
            p6Msg: Union[P6Message, P6Response]):
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
                MessageSenderErrors.WrongSocketType.report(socket.type, zmq.REQ)
            )
        if socket is not None:
            socket.send(msg.toProtoBytes())
            reply = socket.recv()
            replyStr = reply.decode()
            if replyStr.lower() == "ok":
                return Ok(None)
            else:
                return Err(MessageSenderErrors.FailToSend.report("Fail to send: " + str(msg.toProtoObj())))
