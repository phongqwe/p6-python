from typing import Callable

from bicp_document_structure.event.reactor.EventReactor import EventReactor
from bicp_document_structure.event.reactor.cell.CellEventData import CellEventData


class CellEventReactor(EventReactor[CellEventData]):

    def __init__(self, reactorId: str, callback: Callable[[CellEventData], None]):
        self._id = reactorId
        self.callback = callback

    @property
    def id(self) -> str:
        return self._id

    def react(self, cellData: CellEventData):
        self.callback(cellData)
