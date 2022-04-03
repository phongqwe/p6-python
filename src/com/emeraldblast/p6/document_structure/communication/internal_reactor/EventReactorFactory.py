import uuid
from typing import Callable, Any

from com.emeraldblast.p6.document_structure.communication.internal_reactor.BaseReactor import BasicReactor


class EventReactorFactory:
    @staticmethod
    def makeBasicReactor(callback: Callable[[Any], Any]) -> BasicReactor[Any,Any]:
        """create a workbook reactor with randomize uuid4 id"""
        return BasicReactor(str(uuid.uuid4()), callback)