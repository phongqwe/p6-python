from typing import TypeVar

from bicp_document_structure.event.P6Event import P6Event
from bicp_document_structure.event.reactor.EventReactor import EventReactor
from bicp_document_structure.event.reactor.EventReactorContainer import EventReactorContainer, D

D = TypeVar("D")


class MutableEventReactorContainer(EventReactorContainer[D]):

    def __init__(self, innerDict: dict[P6Event, dict[str, EventReactor[D]]] | None = None):
        if innerDict is None:
            innerDict = dict()
        self._dict: dict[P6Event, dict[str, EventReactor[D]]] = innerDict

    def getReactorsForEvent(self, event: P6Event) -> list[EventReactor[D]]:
        rt = self._dict.get(event)
        if rt is not None:
            return list(rt.values())
        else:
            return list()

    def addReactor(self, event: P6Event, reactor: EventReactor[D]) -> "MutableEventReactorContainer":
        reactorMap = self._dict.get(event, dict())
        reactorMap[reactor.id] = reactor
        self._dict[event] = reactorMap
        return self

    def removeReactorsForEvent(self, event: P6Event) -> "MutableEventReactorContainer":
        if self._dict.get(event) is not None:
            del (self._dict[event])
        return self

    def removeReactorById(self, reactorId: str):
        targets = []
        for key in self._dict.keys():
            reactorMap = self._dict.get(key)
            if reactorId in reactorMap:
                targets.append((key, reactorMap))
        for (key, reactorMap) in targets:
            del (reactorMap[reactorId])
            self._dict[key] = reactorMap
        return self

    def removeReactorByEventAndId(self, event: P6Event, id: str) -> "MutableEventReactorContainer":
        reactorMap = self._dict.get(event)
        if reactorMap is not None:
            if id in reactorMap:
                del (reactorMap[id])
        else:
            return self

    def isEmpty(self):
        if len(self._dict) == 0:
            return True
        else:
            for m in self._dict.values():
                if len(m) != 0:
                    return False
            return True
