import uuid
from typing import Callable, TypeVar, Any

from bicp_document_structure.communication.event.reactor.BaseReactor import BasicReactor
from bicp_document_structure.communication.event.reactor.CellReactor import CellReactor
from bicp_document_structure.communication.event.reactor.RangeReactor import RangeReactor
from bicp_document_structure.communication.event.reactor.WorkbookReactor import WorkbookReactor
from bicp_document_structure.communication.event.reactor.WorksheetReactor import WorksheetReactor
from bicp_document_structure.communication.event.reactor.eventData.CellEventData import CellEventData
from bicp_document_structure.communication.event.reactor.eventData.RangeEventData import RangeEventData
from bicp_document_structure.communication.event.reactor.eventData.WorkbookEventData import WorkbookEventData
from bicp_document_structure.communication.event.reactor.eventData.WorksheetEventData import WorksheetEventData


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