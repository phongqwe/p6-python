from abc import ABC

from bicp_document_structure.message.P6Message import P6Message
from bicp_document_structure.message.event.P6Event import P6Event
from bicp_document_structure.message.event.reactor.EventReactor import EventReactor
from bicp_document_structure.util.ToProto import ToProto


class EventServer(ABC):
    """ server accepting requests and sending back responses """

    def start(self,port:int):
        raise NotImplementedError()

    def stop(self):
        raise NotImplementedError()

    def getReactorsForEvent(self, event: P6Event) -> EventReactor[P6Message, ToProto] | None:
        raise NotImplementedError()

    def addReactor(self, event: P6Event, reactor: EventReactor[P6Message, ToProto]):
        raise NotImplementedError()

    def removeReactorsForEvent(self, event: P6Event):
        raise NotImplementedError()

    def isEmpty(self) -> bool:
        raise NotImplementedError()
