from typing import TypeVar

from com.qxdzbc.p6.document_structure.communication.event.P6Event import P6Event
from com.qxdzbc.p6.document_structure.communication.reactor.EventReactor import EventReactor
from com.qxdzbc.p6.document_structure.communication.reactor.EventReactorContainer import EventReactorContainer

D = TypeVar("D")


class MutableEventReactorContainer(EventReactorContainer[D]):

    def __init__(self, innerDict: dict[P6Event, dict[str, EventReactor]] | None = None):
        if innerDict is None:
            innerDict = dict()
        # dict[ event -> dict[reactorId->reactor] ]
        self._dict: dict[P6Event, dict[str, EventReactor]] = innerDict

    def getReactorsForEvent(self, event: P6Event) -> list[EventReactor]:
        rt = self._dict.get(event)
        if rt is not None:
            return list(rt.values())
        else:
            return list()

    def addReactor(self, event: P6Event, reactor: EventReactor) -> "MutableEventReactorContainer":
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