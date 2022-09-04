import uuid
from abc import ABC
from typing import TypeVar

from com.qxdzbc.p6.document_structure.communication.reactor.EventReactor import EventReactor

I = TypeVar("I")
O = TypeVar("O")

class BaseEventReactor(EventReactor[I,O],ABC):
    def __init__(self):
        self._uid=str(uuid.uuid4())

    @property
    def id(self) -> str:
        return self._uid