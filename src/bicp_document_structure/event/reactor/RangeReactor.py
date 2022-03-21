from typing import Callable

from bicp_document_structure.event.P6Event import P6Event
from bicp_document_structure.event.reactor.EventReactor import EventReactor
from bicp_document_structure.event.reactor.eventData.RangeEventData import RangeEventData


class RangeReactor(EventReactor[RangeEventData]):


    def __init__(self, reactorId: str, callback: Callable[[RangeEventData], None],event:P6Event):
        self._id = reactorId
        self.callback = callback
        self._event = event

    @property
    def event(self) -> P6Event:
        return self._event

    @property
    def id(self) -> str:
        return self._id

    def react(self, data: RangeEventData):
        self.callback(data)
