from typing import Callable

from bicp_document_structure.event.reactor.EventReactor import EventReactor
from bicp_document_structure.event.reactor.eventData.ColEventData import ColEventData


class ColumnReactor(EventReactor[ColEventData]):

    def __init__(self, reactorId: str, callback: Callable[[ColEventData], None]):
        self._id = reactorId
        self.callback = callback

    @property
    def id(self) -> str:
        return self._id

    def react(self, data: ColEventData):
        self.callback(data)
