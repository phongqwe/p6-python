from typing import Callable

from bicp_document_structure.event.reactor.EventReactor import EventReactor
from bicp_document_structure.event.reactor.eventData.WorksheetEventData import WorksheetEventData


class WorksheetEventReactor(EventReactor[WorksheetEventData]):

    def __init__(self, reactorId: str, callback: Callable[[WorksheetEventData], None]):
        self._id = reactorId
        self.callback = callback

    @property
    def id(self) -> str:
        return self._id

    def react(self, data: WorksheetEventData):
        self.callback(data)