import uuid
from abc import ABC
from typing import TypeVar, Generic

I = TypeVar("I")
O = TypeVar("O")

class EventReactor(Generic[I,O], ABC):
    """a listener class"""

    @property
    def id(self) -> str:
        raise NotImplementedError()

    def react(self, data: I)->O:
        raise NotImplementedError()
