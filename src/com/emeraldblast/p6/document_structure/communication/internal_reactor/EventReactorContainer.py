from abc import ABC
from typing import TypeVar, Generic

from com.emeraldblast.p6.document_structure.communication.event.P6Event import P6Event
from com.emeraldblast.p6.document_structure.communication.internal_reactor.EventReactor import EventReactor
from com.emeraldblast.p6.document_structure.util.CanCheckEmpty import CanCheckEmpty

D = TypeVar("D")
class EventReactorContainer(Generic[D],CanCheckEmpty,ABC):

    def getReactorsForEvent(self, event: P6Event) -> list[EventReactor]:
        """get all reactors mapped to an event"""
        raise NotImplementedError()

    def addReactor(self, event: P6Event, reactor: EventReactor)->"EventReactorContainer":
        """
        add a reactor for an event
        :return a EventReactorContainer
        """
        raise NotImplementedError()

    def removeReactorsForEvent(self, event: P6Event)->"EventReactorContainer":
        """
        remove all reactors for an event
        :return a EventReactorContainer
        """
        raise NotImplementedError()

    def removeReactorById(self, reactorId: str)->"EventReactorContainer":
        """
        remove all reactors have ids that match the input id
        :return a EventReactorContainer
        """
        raise NotImplementedError()

    def removeReactorByEventAndId(self, event: P6Event, reactorId: str)->"EventReactorContainer":
        """
        remove a reactor with a reactor id, mapped to an event
        :return a EventReactorContainer
        """
        raise NotImplementedError()

    def triggerReactorsFor(self,event:P6Event, data:D):
        """trigger all reactor of an event with a piece of data"""
        reactorList:list[EventReactor] = self.getReactorsForEvent(event)
        for reactor in reactorList:
            reactor.react(data)
