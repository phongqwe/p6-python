from typing import Callable

from com.emeraldblast.p6.document_structure.communication.internal_reactor.EventReactor import EventReactor
from com.emeraldblast.p6.document_structure.communication.internal_reactor.eventData.WorksheetEventData import WorksheetEventData


class WorksheetReactor(EventReactor[WorksheetEventData,None]):

    def __init__(self, reactorId: str, callback: Callable[[WorksheetEventData], None]):
        self._id = reactorId
        self._callback = callback

    @property
    def id(self) -> str:
        return self._id

    def react(self, data: WorksheetEventData):
        self._callback(data)
