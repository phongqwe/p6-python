from abc import ABC
from typing import TypeVar, Generic

from bicp_document_structure.event.P6Event import P6Event

D = TypeVar("D")


class EventReactor(Generic[D], ABC):
    """a listener class"""

    @property
    def id(self) -> str:
        raise NotImplementedError()

    @property
    def event(self) -> P6Event:
        raise NotImplementedError()

    def react(self, data: D):
        raise NotImplementedError()
