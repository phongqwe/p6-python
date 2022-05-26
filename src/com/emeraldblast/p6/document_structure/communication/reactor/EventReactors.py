import uuid
from typing import Callable, Any

from com.emeraldblast.p6.document_structure.communication.reactor.BaseReactor import BaseReactor


class EventReactors:
    @staticmethod
    def makeBasicReactor(callback: Callable[[Any], Any]) -> BaseReactor[Any, Any]:
        """create a workbook reactor with randomize uuid4 id"""
        return BaseReactor(str(uuid.uuid4()), callback)