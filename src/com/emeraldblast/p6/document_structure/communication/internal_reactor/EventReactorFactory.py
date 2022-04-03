import uuid
from typing import Callable, Any

from com.emeraldblast.p6.document_structure.communication.internal_reactor.BaseReactor import BasicReactor
from com.emeraldblast.p6.document_structure.communication.internal_reactor.CellReactor import CellReactor
from com.emeraldblast.p6.document_structure.communication.internal_reactor.RangeReactor import RangeReactor
from com.emeraldblast.p6.document_structure.communication.internal_reactor.WorkbookReactor import WorkbookReactor
from com.emeraldblast.p6.document_structure.communication.internal_reactor.WorksheetReactor import WorksheetReactor
from com.emeraldblast.p6.document_structure.communication.internal_reactor.eventData.CellEventData import CellEventData
from com.emeraldblast.p6.document_structure.communication.internal_reactor.eventData.RangeEventData import RangeEventData
from com.emeraldblast.p6.document_structure.communication.internal_reactor.eventData.WorkbookEventData import WorkbookEventData
from com.emeraldblast.p6.document_structure.communication.internal_reactor.eventData.WorksheetEventData import WorksheetEventData


class EventReactorFactory:
    @staticmethod
    def makeCellReactor(callback:Callable[[CellEventData], None]) -> CellReactor:
        """create a cell reactor with randomize uuid4 id"""
        return CellReactor(str(uuid.uuid4()), callback)

    @staticmethod
    def makeRangeReactor(callback: Callable[[RangeEventData], None]) -> RangeReactor:
        """create a range reactor with randomize uuid4 id"""
        return RangeReactor(str(uuid.uuid4()), callback)

    @staticmethod
    def makeWorksheetReactor(callback: Callable[[WorksheetEventData], None]) -> WorksheetReactor:
        """create a worksheet reactor with randomize uuid4 id"""
        return WorksheetReactor(str(uuid.uuid4()), callback)

    @staticmethod
    def makeWorkbookReactor(callback: Callable[[WorkbookEventData], None]) -> WorkbookReactor:
        """create a workbook reactor with randomize uuid4 id"""
        return WorkbookReactor(str(uuid.uuid4()), callback)
    @staticmethod
    def makeBasicReactor(callback: Callable[[Any], Any]) -> BasicReactor[Any,Any]:
        """create a workbook reactor with randomize uuid4 id"""
        return BasicReactor(str(uuid.uuid4()), callback)