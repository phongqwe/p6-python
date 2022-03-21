from abc import ABC
from typing import TypeVar, Generic

D = TypeVar("D")


class EventReactor(Generic[D], ABC):
    """a listener class"""

    @property
    def id(self) -> str:
        raise NotImplementedError()

    # @property
    # def event(self) -> P6Event:
    #     raise NotImplementedError()

    def react(self, data: D):
        raise NotImplementedError()
