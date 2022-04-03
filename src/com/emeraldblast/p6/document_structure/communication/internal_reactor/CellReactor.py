from typing import Callable

from com.emeraldblast.p6.document_structure.communication.internal_reactor.EventReactor import EventReactor
from com.emeraldblast.p6.document_structure.communication.internal_reactor.eventData.CellEventData import CellEventData


class CellReactor(EventReactor[CellEventData,None]):

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
