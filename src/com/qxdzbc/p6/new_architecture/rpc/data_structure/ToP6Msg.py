from abc import ABC

from com.qxdzbc.p6.new_architecture.communication.P6Messages import P6Messages
from com.qxdzbc.p6.new_architecture.communication.msg.P6Message import P6Message
from com.qxdzbc.p6.document_structure.util.ToProto import ToProto


class ToP6Msg(ToProto, ABC):
    """
    a mixin providing ability to turn itself into a P6Message. Event is looked up automatically
    """

    def toP6Msg(self) -> P6Message:
        from com.qxdzbc.p6.new_architecture.communication import P6EventTableImp
        event = P6EventTableImp.i().getEventFor(self)
        return P6Messages.p6Message(
            event = event,
            data = self,
        )
