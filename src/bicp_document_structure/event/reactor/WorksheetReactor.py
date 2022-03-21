from typing import Callable

from bicp_document_structure.event.P6Event import P6Event
from bicp_document_structure.event.reactor.EventReactor import EventReactor
from bicp_document_structure.event.reactor.eventData.WorksheetEventData import WorksheetEventData


class WorksheetReactor(EventReactor[WorksheetEventData]):

    def __init__(self, reactorId: str, callback: Callable[[WorksheetEventData], None], event:P6Event):
        self._id = reactorId
        self._callback = callback
        self._event = event

    @property
    def event(self) -> P6Event:
        return self._event

    @property
    def id(self) -> str:
        return self._id

    def react(self, data: WorksheetEventData):
        self._callback(data)
