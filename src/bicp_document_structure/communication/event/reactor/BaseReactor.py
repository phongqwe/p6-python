from typing import TypeVar, Callable

from bicp_document_structure.communication.event.reactor.EventReactor import EventReactor

I = TypeVar("I")
O = TypeVar("O")
class BasicReactor(EventReactor[I, O]):

    def __init__(self, reactorId: str, callback: Callable[[I], O]):
        self._id = reactorId
        self.callback: Callable[[I], O] = callback

    @property
    def id(self) -> str:
        return self._id

    def react(self, data: I) -> O:
        return self.callback(data)
