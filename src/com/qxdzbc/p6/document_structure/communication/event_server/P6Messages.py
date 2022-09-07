import uuid

from com.qxdzbc.p6.document_structure.communication.event.P6Event import P6Event
from com.qxdzbc.p6.document_structure.communication.event_server.msg.P6Message import P6Message
from com.qxdzbc.p6.document_structure.communication.event_server.msg.P6MessageHeader import P6MessageHeader
from com.qxdzbc.p6.document_structure.communication.event_server.response.P6Response import P6Response
from com.qxdzbc.p6.document_structure.util.ToProto import ToProto


class P6Messages:
    @staticmethod
    def p6Response(event: P6Event, data: ToProto | str | bytes, status: P6Response.Status = P6Response.Status.OK):
        res = P6Response(
            header = P6MessageHeader(
                msgId = str(uuid.uuid4()),
                eventType = event,
            ),
            status = status,
            data = data
        )
        return res

    @staticmethod
    def p6Message(event: P6Event, data: ToProto | str | bytes, ):
        msg = P6Message(
            header = P6MessageHeader(
                msgId = str(uuid.uuid4()),
                eventType = event,
            ),
            data = data)
        return msg