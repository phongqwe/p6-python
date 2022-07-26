from abc import ABC
from typing import Optional

from com.emeraldblast.p6.document_structure.communication.event.P6Event import P6Event
from com.emeraldblast.p6.document_structure.communication.event_server.msg.P6Message import P6Message
from com.emeraldblast.p6.document_structure.communication.reactor.EventReactor import EventReactor
from com.emeraldblast.p6.document_structure.util.ToProto import ToProto


class EventServer(ABC):
    """
     a server accepting requests (in P6Message) from front end and sending back responses (in P6Response)
     """

    def start(self,port:int):
        raise NotImplementedError()

    def stop(self):
        raise NotImplementedError()

    def getReactorsForEvent(self, event: P6Event) -> Optional[EventReactor[P6Message, ToProto]]:
        raise NotImplementedError()

    def addReactor(self, event: P6Event, reactor: EventReactor[P6Message, ToProto]):
        raise NotImplementedError()

    def removeReactorsForEvent(self, event: P6Event):
        raise NotImplementedError()

    def isEmpty(self) -> bool:
        raise NotImplementedError()
