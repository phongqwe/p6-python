from typing import Callable

from bicp_document_structure.message.event.reactor.EventReactor import EventReactor
from bicp_document_structure.message.event.reactor.eventData.CellEventData import CellEventData


class CellReactor(EventReactor[CellEventData]):

    # @property
    # def event(self) -> P6Event:
    #     return self._event

    def __init__(self, reactorId: str, callback: Callable[[CellEventData], None]):
        self._id = reactorId
        self.callback = callback
        # self._event = event

    @property
    def id(self) -> str:
        return self._id

    def react(self, cellData: CellEventData):
        self.callback(cellData)
