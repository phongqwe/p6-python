from typing import TypeVar

from bicp_document_structure.event.P6Event import P6Event
from bicp_document_structure.event.reactor.EventReactor import EventReactor
from bicp_document_structure.event.reactor.EventReactorContainer import EventReactorContainer
from bicp_document_structure.event.reactor.MutableEventReactorContainer import MutableEventReactorContainer

D = TypeVar("D")


class EventReactorContainers:
    @staticmethod
    def mutable(initDict: dict[P6Event, dict[str, EventReactor[D]]] | None = None) -> EventReactorContainer:
        if initDict is None:
            initDict = dict()
        return MutableEventReactorContainer(initDict)
