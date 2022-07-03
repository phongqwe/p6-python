from abc import ABC
from typing import TypeVar

from com.emeraldblast.p6.document_structure.communication.event.P6EventTable import P6EventTable
from com.emeraldblast.p6.document_structure.communication.notifier.eventData.EventData import EventData
from com.emeraldblast.p6.document_structure.util.ToProto import ToProto




class ToEventData(ToProto,ABC):
    def toEventData(self)->EventData:
        from com.emeraldblast.p6.document_structure.communication.event.P6EventTableImp import P6EventTableImp
        eventTable: P6EventTable = P6EventTableImp.i()
        return EventData(
            event = eventTable.getEventFor(self),
            data = self
        )
