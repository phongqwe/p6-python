from abc import ABC
from typing import Any, Type

from com.qxdzbc.p6.document_structure.communication.event.P6Event import P6Event


# if TYPE_CHECKING:


class P6EventTable(ABC):
    def getEventFor(self, something: Any) -> P6Event:
        raise NotImplementedError()

    def getEventForClazz(self, clazz: Type) -> P6Event:
        raise NotImplementedError()



