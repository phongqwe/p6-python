from typing import TypeVar

from com.emeraldblast.p6.document_structure.communication.event.P6Event import P6Event
from com.emeraldblast.p6.document_structure.communication.internal_reactor.EventReactor import EventReactor
from com.emeraldblast.p6.document_structure.communication.internal_reactor.EventReactorContainer import EventReactorContainer
from com.emeraldblast.p6.document_structure.communication.internal_reactor.MutableEventReactorContainer import MutableEventReactorContainer

D = TypeVar("D")


class EventReactorContainers:
    @staticmethod
    def mutable(initDict: dict[P6Event, dict[str, EventReactor]] | None = None) -> EventReactorContainer:
        if initDict is None:
            initDict = dict()
        return MutableEventReactorContainer(initDict)
