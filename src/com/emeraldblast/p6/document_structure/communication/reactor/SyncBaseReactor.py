from threading import RLock
from typing import TypeVar, Callable, Generic

from com.emeraldblast.p6.document_structure.communication.reactor.EventReactor import EventReactor

I = TypeVar("I")
O = TypeVar("O")
class SyncBaseReactor(EventReactor[I, O], Generic[I, O]):

    def __init__(self, reactorId: str, callback: Callable[[I], O]):
        self.lock = RLock()
        self._id = reactorId
        self.callback: Callable[[I], O] = callback

    @property
    def id(self) -> str:
        return self._id

    def react(self, data: I) -> O:
        with self.lock:
            return self.callback(data)