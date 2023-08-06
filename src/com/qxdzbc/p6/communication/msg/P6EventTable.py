from abc import ABC
from typing import Any, Type



# if TYPE_CHECKING:
from com.qxdzbc.p6.communication.msg.P6Event import P6Event


class P6EventTable(ABC):
    def getEventFor(self, something: Any) -> P6Event:
        raise NotImplementedError()

    def getEventForClazz(self, clazz: Type) -> P6Event:
        raise NotImplementedError()



