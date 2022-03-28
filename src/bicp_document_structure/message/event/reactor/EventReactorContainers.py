from typing import TypeVar

from bicp_document_structure.message.event.P6Event import P6Event
from bicp_document_structure.message.event.reactor.EventReactor import EventReactor
from bicp_document_structure.message.event.reactor.EventReactorContainer import EventReactorContainer
from bicp_document_structure.message.event.reactor.MutableEventReactorContainer import MutableEventReactorContainer

D = TypeVar("D")


class EventReactorContainers:
    @staticmethod
    def mutable(initDict: dict[P6Event, dict[str, EventReactor]] | None = None) -> EventReactorContainer:
        if initDict is None:
            initDict = dict()
        return MutableEventReactorContainer(initDict)
