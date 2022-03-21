import uuid
from typing import Callable

from bicp_document_structure.event.P6Event import P6Event
from bicp_document_structure.event.reactor.CellReactor import CellReactor
from bicp_document_structure.event.reactor.ColumnReactor import ColumnReactor
from bicp_document_structure.event.reactor.RangeReactor import RangeReactor
from bicp_document_structure.event.reactor.WorkbookReactor import WorkbookReactor
from bicp_document_structure.event.reactor.WorksheetReactor import WorksheetReactor
from bicp_document_structure.event.reactor.eventData.CellEventData import CellEventData
from bicp_document_structure.event.reactor.eventData.ColEventData import ColEventData
from bicp_document_structure.event.reactor.eventData.RangeEventData import RangeEventData
from bicp_document_structure.event.reactor.eventData.WorkbookEventData import WorkbookEventData
from bicp_document_structure.event.reactor.eventData.WorksheetEventData import WorksheetEventData


class EventReactorFactory:
    @staticmethod
    def makeCellReactor(callback:Callable[[CellEventData], None],event:P6Event) -> CellReactor:
        """create a cell reactor with randomize uuid4 id"""
        return CellReactor(str(uuid.uuid4()), callback,event)

    @staticmethod
    def makeColReactor(callback: Callable[[ColEventData], None]) -> ColumnReactor:
        """create a col reactor with randomize uuid4 id"""
        return ColumnReactor(str(uuid.uuid4()), callback)

    @staticmethod
    def makeRangeReactor(callback: Callable[[RangeEventData], None],event:P6Event) -> RangeReactor:
        """create a range reactor with randomize uuid4 id"""
        return RangeReactor(str(uuid.uuid4()), callback,event)

    @staticmethod
    def makeWorksheetReactor(callback: Callable[[WorksheetEventData], None],event:P6Event) -> WorksheetReactor:
        """create a worksheet reactor with randomize uuid4 id"""
        return WorksheetReactor(str(uuid.uuid4()), callback,event)

    @staticmethod
    def makeWorkbookReactor(callback: Callable[[WorkbookEventData], None],event:P6Event) -> WorkbookReactor:
        """create a workbook reactor with randomize uuid4 id"""
        return WorkbookReactor(str(uuid.uuid4()), callback,event)