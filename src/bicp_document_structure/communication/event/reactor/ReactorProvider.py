from abc import ABC

from bicp_document_structure.communication.event.reactor.CellReactor import CellReactor
from bicp_document_structure.communication.event.reactor.RangeReactor import RangeReactor
from bicp_document_structure.communication.event.reactor.WorkbookReactor import WorkbookReactor
from bicp_document_structure.communication.event.reactor.WorksheetReactor import WorksheetReactor


class ReactorProvider(ABC):
    def createNewWorksheet(self)->WorkbookReactor:
        raise NotImplementedError()

    def cellUpdateReactor(self) -> CellReactor:
        raise NotImplementedError()

    def rangeReRun(self) -> RangeReactor:
        raise NotImplementedError()

    def worksheetReRun(self) -> WorksheetReactor:
        raise NotImplementedError()

    def worksheetRename(self) -> WorkbookReactor:
        raise NotImplementedError()

    def workbookReRun(self) -> WorkbookReactor:
        raise NotImplementedError()
