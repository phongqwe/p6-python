import uuid
from typing import Callable, Any

from com.qxdzbc.p6.document_structure.communication.reactor.BaseReactor import BaseReactor
from com.qxdzbc.p6.document_structure.communication.reactor.EventReactor import EventReactor
from com.qxdzbc.p6.document_structure.communication.reactor.SyncBaseReactor import SyncBaseReactor


class EventReactors:
    @staticmethod
    def makeBasicReactor(callback: Callable[[Any], Any]) -> BaseReactor[Any, Any]:
        """create a workbook reactor with randomize uuid4 id"""
        return BaseReactor(str(uuid.uuid4()), callback)

    @staticmethod
    def makeSyncBasicReactor(callback: Callable[[Any], Any]) -> SyncBaseReactor[Any, Any]:
        """create a workbook reactor with randomize uuid4 id"""
        return SyncBaseReactor(str(uuid.uuid4()), callback)