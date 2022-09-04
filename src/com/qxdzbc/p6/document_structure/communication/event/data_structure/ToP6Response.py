from abc import ABC

from com.qxdzbc.p6.document_structure.communication.event_server.P6Messages import P6Messages
from com.qxdzbc.p6.document_structure.communication.event_server.response.P6Response import P6Response
from com.qxdzbc.p6.document_structure.util.ToProto import ToProto


class ToP6Response(ToProto, ABC):
    """
    a mixin providing ability to turn itself into a P6Message. Event is looked up automatically
    """

    def toP6Msg(self) -> P6Response:
        from com.qxdzbc.p6.document_structure.communication.event.P6EventTableImp import P6EventTableImp
        event = P6EventTableImp.i().getEventFor(self)
        return P6Messages.p6Response(
            event = event,
            data = self,
        )
