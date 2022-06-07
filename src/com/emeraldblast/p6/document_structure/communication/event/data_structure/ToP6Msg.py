from abc import ABC

from com.emeraldblast.p6.document_structure.communication.event import P6EventTable
from com.emeraldblast.p6.document_structure.communication.event_server.P6Messages import P6Messages
from com.emeraldblast.p6.document_structure.communication.event_server.msg.P6Message import P6Message
from com.emeraldblast.p6.document_structure.util.ToProto import ToProto


class ToP6Msg(ToProto, ABC):
    def toP6Msg(self)->P6Message:
        from com.emeraldblast.p6.document_structure.communication.event.P6EventTableImp import P6EventTableImp
        eventTable: P6EventTable = P6EventTableImp.i()
        return P6Messages.p6Message(
            event=eventTable.getEventFor(self),
            data = self
        )