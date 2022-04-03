from typing import Callable, TypeVar

from com.emeraldblast.p6.document_structure.communication.internal_reactor.EventReactor import EventReactor
from com.emeraldblast.p6.document_structure.communication.internal_reactor.eventData.WorkbookEventData import WorkbookEventData

OutType = TypeVar("OutType")


class WorkbookReactor(EventReactor[WorkbookEventData, OutType]):

    def __init__(self, reactorId: str, callback: Callable[[WorkbookEventData], OutType]):
        self._id = reactorId
        self.callback: Callable[[WorkbookEventData], OutType] = callback

    @property
    def id(self) -> str:
        return self._id

    def react(self, data: WorkbookEventData) -> OutType:
        return self.callback(data)
