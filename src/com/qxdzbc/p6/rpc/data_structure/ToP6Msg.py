from abc import ABC

from com.qxdzbc.p6.communication.msg.P6Message import P6Message
from com.qxdzbc.p6.util.ToProto import ToProto
from com.qxdzbc.p6.communication.P6Messages import P6Messages


class ToP6Msg(ToProto, ABC):
    """
    a mixin providing ability to turn itself into a P6Message. Event is looked up automatically
    """

    def toP6Msg(self) -> P6Message:
        from com.qxdzbc.p6.communication.msg.P6EventTableImp import P6EventTableImp
        event = P6EventTableImp.i().getEventFor(self)
        return P6Messages.p6Message(
            event = event,
            data = self,
        )
